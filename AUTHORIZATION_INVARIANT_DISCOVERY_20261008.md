# Authorization Invariant Discovery — 2026-10-08

Cross-project security theorem and executable reference model.

\[
\mathrm{Invoke}\Rightarrow
\mathrm{BoundPrincipal}\land
\mathrm{BoundTask}\land
\mathrm{BoundTool}\land
\mathrm{BoundArgs}\land
\mathrm{Fresh}\land
\mathrm{ActivePrincipal}.
\]

Successful invocation consumes a nonce. Replay, cross-task reuse, cross-principal reuse, tool substitution, argument substitution, stale/pre-issued use, inactive-principal use, and signature-only authorization are rejected by the reference state machine.

Executed reference-model result: **16/16 PASS**.

Canonical implementation and proof:
- https://github.com/nicholaskouns-create/auth-kernel
- https://github.com/nicholaskouns-create/E47-Kartekeya/blob/main/research/security/AUTHORIZATION_INVARIANT_DISCOVERY_20261008.md

Evidence boundary: this records the formal invariant and reference-model validation. Direct regression against each upstream implementation remains a separate evidence layer.
