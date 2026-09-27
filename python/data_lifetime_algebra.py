# MARK: FOUNDRY-LIFETIME-E47-INTERSECTION / FOUNDRY-ALGEBRA
# Kernel lock: dimH=125 dimE47=47 rankK=78 Omega_c=47/125
#!/usr/bin/env python3
"""Foundry Data Lifetime policy algebra: stamp, inherit, override."""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Dict, Iterable, List, Optional, Set

UTC = timezone.utc
BOT = datetime.min.replace(tzinfo=UTC)

class TxKind(str, Enum):
    SNAPSHOT = "SNAPSHOT"
    APPEND = "APPEND"
    UPDATE = "UPDATE"
    DELETE = "DELETE"

class PolicyKind(str, Enum):
    FIXED = "fixed"
    LATEST_VIEW_ONLY = "latest_view_only"

@dataclass(frozen=True)
class Transaction:
    dataset: str
    tx_id: str
    t: datetime
    branch: str
    kind: TxKind = TxKind.SNAPSHOT

@dataclass
class Policy:
    kind: PolicyKind
    name: str
    deletion_at: Optional[datetime] = None
    cutoff: Optional[datetime] = None
    branches: Optional[Set[str]] = None
    def __post_init__(self) -> None:
        if self.kind is PolicyKind.FIXED and self.deletion_at is None:
            raise ValueError("fixed policy requires deletion_at")
        if self.kind is PolicyKind.LATEST_VIEW_ONLY and not self.branches:
            raise ValueError("latest_view_only policy requires branches")

@dataclass
class Override:
    dataset: str
    replacement: Optional[Policy] = None

@dataclass
class Graph:
    transactions: Dict[str, Transaction] = field(default_factory=dict)
    parents: Dict[str, Set[str]] = field(default_factory=dict)
    children: Dict[str, Set[str]] = field(default_factory=dict)
    order: List[str] = field(default_factory=list)
    def add(self, tx: Transaction, parent_ids: Iterable[str] = ()) -> None:
        if tx.tx_id in self.transactions:
            raise ValueError(f"duplicate transaction {tx.tx_id}")
        self.transactions[tx.tx_id] = tx
        self.order.append(tx.tx_id)
        self.parents.setdefault(tx.tx_id, set())
        self.children.setdefault(tx.tx_id, set())
        for p in parent_ids:
            if p not in self.transactions:
                raise ValueError(f"unknown parent {p}")
            self.parents[tx.tx_id].add(p)
            self.children.setdefault(p, set()).add(tx.tx_id)
    def txs_on(self, dataset: str) -> List[Transaction]:
        return [self.transactions[i] for i in self.order if self.transactions[i].dataset == dataset]
    def descendants(self, tx_id: str) -> Set[str]:
        out: Set[str] = set()
        stack = list(self.children.get(tx_id, ()))
        while stack:
            n = stack.pop()
            if n in out:
                continue
            out.add(n)
            stack.extend(self.children.get(n, ()))
        return out

def _aware(t: datetime) -> datetime:
    return t if t.tzinfo is not None else t.replace(tzinfo=UTC)

def view_membership(g: Graph, dataset: str, branch: str) -> Set[str]:
    live: Set[str] = set()
    for tx in g.txs_on(dataset):
        if tx.branch != branch:
            continue
        if tx.kind is TxKind.SNAPSHOT:
            live = {tx.tx_id}
        elif tx.kind in (TxKind.APPEND, TxKind.UPDATE):
            live.add(tx.tx_id)
        elif tx.kind is TxKind.DELETE:
            live.discard(tx.tx_id)
    return live

def stamp_fixed(g: Graph, dataset: str, policy: Policy) -> Dict[str, Optional[datetime]]:
    T = _aware(policy.deletion_at)
    C = _aware(policy.cutoff) if policy.cutoff else None
    out: Dict[str, Optional[datetime]] = {}
    for tx in g.txs_on(dataset):
        out[tx.tx_id] = T if (C is None or _aware(tx.t) < C) else None
    return out

def stamp_latest_view_only(g: Graph, dataset: str, policy: Policy) -> Dict[str, Optional[datetime]]:
    B = set(policy.branches)
    txs = g.txs_on(dataset)
    newest = max((_aware(tx.t) for tx in txs), default=BOT)
    out: Dict[str, Optional[datetime]] = {}
    for tx in txs:
        if any(tx.tx_id in view_membership(g, tx.dataset, b) for b in B):
            out[tx.tx_id] = None
        elif tx.branch not in B:
            out[tx.tx_id] = _aware(tx.t)
        else:
            out[tx.tx_id] = newest
    return out

def stamp_root(g: Graph, dataset: str, policy: Policy) -> Dict[str, Optional[datetime]]:
    if policy.kind is PolicyKind.FIXED:
        return stamp_fixed(g, dataset, policy)
    return stamp_latest_view_only(g, dataset, policy)

def _combine(dates: List[Optional[datetime]]) -> Optional[datetime]:
    present = [d for d in dates if d is not None]
    return min(present) if present else None

def inherit(g: Graph, root_delta: Dict[str, Optional[datetime]]) -> Dict[str, Optional[datetime]]:
    delta: Dict[str, Optional[datetime]] = {tx_id: None for tx_id in g.transactions}
    seeds = set(root_delta)
    delta.update(root_delta)
    changed = True
    while changed:
        changed = False
        for tx_id in g.order:
            if tx_id in seeds:
                continue
            pars = g.parents.get(tx_id, set())
            if not pars:
                continue
            new = _combine([delta[p] for p in pars])
            if delta[tx_id] != new:
                delta[tx_id] = new
                changed = True
    return delta

def apply_override(g: Graph, delta: Dict[str, Optional[datetime]], ov: Override) -> Dict[str, Optional[datetime]]:
    cone = {tx.tx_id for tx in g.txs_on(ov.dataset)}
    for tx_id in list(cone):
        cone |= g.descendants(tx_id)
    out = dict(delta)
    for tx_id in cone:
        out[tx_id] = None
    if ov.replacement is None:
        return out
    reseed = stamp_root(g, ov.dataset, ov.replacement)
    out.update(reseed)
    pushed = inherit(g, reseed)
    for tx_id in cone:
        out[tx_id] = pushed.get(tx_id)
    return out

def evaluate(g: Graph, attachments: Dict[str, Policy], overrides: Iterable[Override] = ()) -> Dict[str, Optional[datetime]]:
    delta: Dict[str, Optional[datetime]] = {}
    for dataset, policy in attachments.items():
        delta.update(stamp_root(g, dataset, policy))
    delta = inherit(g, delta)
    for ov in overrides:
        delta = apply_override(g, delta, ov)
    return delta

def condemned(delta: Dict[str, Optional[datetime]], now: datetime) -> Set[str]:
    now = _aware(now)
    return {tx_id for tx_id, d in delta.items() if d is not None and d <= now}
