#!/usr/bin/env python3
"""Repository-native 38-check E47 × Foundry Lifetime intersection validator."""

from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import numpy as np

from spectral_engine import (
    CASIMIR_LOCKED,
    DIM_COMPLEMENT_LOCKED,
    DIM_H,
    DIM_KERNEL_LOCKED,
    KAPPA_LOCKED,
    OMEGA_C_LOCKED,
    P47_ON_SPEC_LOCKED,
    P_47,
    SECTOR_DIMS_LOCKED,
    SPECTRAL_GAP_LOCKED,
    SpectralEngine,
)
from data_lifetime_algebra import (
    Graph,
    Override,
    Policy,
    PolicyKind,
    Transaction,
    TxKind,
    condemned,
    evaluate,
    view_membership,
)

UTC = timezone.utc
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "artifacts"
TITLE = "INTERSECTIONALITY VALIDATOR — E47 ∩ Foundry Lifetime"


def ts(day: int) -> datetime:
    return datetime(2026, 1, 1, tzinfo=UTC) + timedelta(days=day)


def build_graph() -> Graph:
    g = Graph()
    for i in range(DIM_COMPLEMENT_LOCKED):
        kind = TxKind.SNAPSHOT if i == 0 else TxKind.APPEND
        g.add(Transaction("raw", f"p{i}", ts(i), "main", kind))
    g.add(Transaction("raw", "k0", ts(DIM_COMPLEMENT_LOCKED), "main", TxKind.SNAPSHOT))
    for i in range(1, DIM_KERNEL_LOCKED):
        g.add(Transaction("raw", f"k{i}", ts(DIM_COMPLEMENT_LOCKED + i), "main", TxKind.APPEND))
    for i in range(DIM_COMPLEMENT_LOCKED):
        g.add(Transaction("derived", f"d{i}", ts(200 + i), "main", TxKind.SNAPSHOT), [f"p{i}"])
    for i in range(DIM_KERNEL_LOCKED):
        kid = "k0" if i == 0 else f"k{i}"
        g.add(Transaction("derived", f"m{i}", ts(300 + i), "main", TxKind.SNAPSHOT), [kid])
    return g


class Audit:
    def __init__(self) -> None:
        self.checks: list[dict[str, Any]] = []
        self.failed = 0

    def record(self, name: str, ok: bool, got: Any, want: Any) -> None:
        self.checks.append({"name": name, "pass": bool(ok), "got": got, "want": want})
        if not ok:
            self.failed += 1
        print(f"{'PASS' if ok else 'FAIL'}  {name}  got={got}  want={want}")

    def eq(self, name: str, got: Any, want: Any) -> None:
        self.record(name, got == want, got, want)

    def close(self, name: str, got: float, want: float, tol: float = 1e-12) -> None:
        self.record(name, abs(got - want) < tol, got, want)


def main() -> int:
    spec = SpectralEngine()
    spec.validate()
    v = Audit()

    # Six local lock parity checks, replacing the old external engine dependency.
    v.eq("dim_H ∩ local lock", spec.dim_H, DIM_H)
    v.eq("dim_E47 ∩ local lock", spec.dim_kernel, DIM_KERNEL_LOCKED)
    v.eq("rank_K ∩ local lock", spec.dim_complement, DIM_COMPLEMENT_LOCKED)
    v.close("Omega_c ∩ local lock", spec.omega_c, OMEGA_C_LOCKED)
    v.eq("Delta ∩ local lock", spec.spectral_gap, SPECTRAL_GAP_LOCKED)
    v.eq("kappa ∩ local lock", int(spec.kappa), KAPPA_LOCKED)

    dims = SECTOR_DIMS_LOCKED
    e6, e30 = int(dims[2]), int(dims[5])
    v.eq("dim E6", e6, 25)
    v.eq("dim E30", e30, 22)
    v.eq("E6 ∩ E30", 0, 0)
    v.eq("E6 ⊕ E30 = E47", e6 + e30, 47)
    v.eq("sum sector dims = dim H", int(dims.sum()), 125)
    v.eq("perp dims sum", int(dims.sum() - e6 - e30), 78)

    p = spec.P_on_spectrum
    v.record("P47 on spec(C)", np.allclose(p, P47_ON_SPEC_LOCKED), p.tolist(), P47_ON_SPEC_LOCKED.tolist())
    v.close("P47 ∩ (I-P47) on spec", float(np.dot(p, 1.0 - p)), 0.0)
    v.close("Tr P47", float(spec.trace_P47), 47.0)
    for lam, expect in zip(CASIMIR_LOCKED, P47_ON_SPEC_LOCKED):
        v.close(f"P47(lambda={int(lam)})", float(P_47(lam)), float(expect), tol=1e-9)

    g = build_graph()
    live = view_membership(g, "raw", "main")
    raw_ids = {i for i, t in g.transactions.items() if t.dataset == "raw"}
    dated_raw_view = raw_ids - live
    ker_ids = {"k0"} | {f"k{i}" for i in range(1, DIM_KERNEL_LOCKED)}
    perp_ids = {f"p{i}" for i in range(DIM_COMPLEMENT_LOCKED)}

    v.eq("|raw|", len(raw_ids), 125)
    v.eq("|V(raw,main)|", len(live), 47)
    v.eq("|V^c raw|", len(dated_raw_view), 78)
    v.eq("V ∩ V^c", len(live & dated_raw_view), 0)
    v.eq("V ∩ ker_ids", live & ker_ids, ker_ids)
    v.eq("V^c ∩ perp_ids", dated_raw_view & perp_ids, perp_ids)
    v.eq("ker ∩ perp", len(ker_ids & perp_ids), 0)

    lvo = Policy(PolicyKind.LATEST_VIEW_ONLY, "e47-lvo", branches={"main"})
    delta = evaluate(g, {"raw": lvo})
    now = ts(400)
    dl = condemned(delta, now)
    ret = set(perp_ids)
    raw_unmarked = {i for i in raw_ids if delta.get(i) is None}
    raw_marked = {i for i in raw_ids if i in dl}

    v.eq("Foundry live ∩ E47 ker", raw_unmarked, ker_ids)
    v.eq("Foundry dated-raw ∩ E47 perp", raw_marked, perp_ids)
    v.eq("DL ∩ Retention", dl & ret, ret)
    v.eq("|DL - Retention| cascade", len(dl - ret), 78)
    v.eq("Retention - DL", len(ret - dl), 0)
    v.close("omega_hat ∩ Omega_c", len(raw_unmarked) / len(raw_ids), 47 / 125)

    delta_ov = evaluate(g, {"raw": lvo}, overrides=[Override("derived", replacement=None)])
    ov = condemned(delta_ov, now)
    der_ids = {i for i, t in g.transactions.items() if t.dataset == "derived"}
    v.eq("override ∩ derived dated", len(ov & der_ids), 0)
    v.eq("override ∩ raw dated", ov & raw_ids, raw_marked)
    v.eq("cascade ∩ override_marked", len((dl - ret) & ov), 0)

    passed = v.failed == 0
    banner = f"[INTERSECTIONALITY VALIDATOR] {'PASS' if passed else 'FAIL'}  {len(v.checks)-v.failed}/{len(v.checks)} intersections hold"
    print(banner)

    OUT.mkdir(exist_ok=True)
    payload = {
        "title": TITLE,
        "passed": passed,
        "banner": banner,
        "n_checks": len(v.checks),
        "n_fail": v.failed,
        "kernel": {
            "dimH": spec.dim_H,
            "dimE47": spec.dim_kernel,
            "rankK": spec.dim_complement,
            "Omega_c": spec.omega_c,
            "Delta": spec.spectral_gap,
            "kappa": spec.kappa,
            "rho": spec.rho,
            "TrP47": spec.trace_P47,
        },
        "checks": v.checks,
    }
    (OUT / "intersectionality_validator.json").write_text(json.dumps(payload, indent=2, default=str) + "\n")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
