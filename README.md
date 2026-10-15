# FOUNDRY-LIFETIME-E47-INTERSECTION

> **Main entry portal:** [The Mathematical City](https://nicholaskouns-create.github.io/website/) — explore the districts, interactive labs, and research index.
>
> **[Explore PiP Manta](https://nicholaskouns-create.github.io/E47-Kartekeya/interfaces/pip-manta/embed.html)**

**Mark:** Foundry Data Lifetime algebra run through the locked E47 kernel.  
**Owner:** Nicholas Kouns (`nicholaskouns-create`)  
**Kernel authority:** [E47-Kartekeya](https://github.com/nicholaskouns-create/E47-Kartekeya)

`K=(C-6I)(C-30I)`, `dim H=125`, `dim E47=47`, `Omega_c=47/125`.

## 2026-10-08 corrected Grassmann–Casimir authority

The canonical spin-2 triple statement is [E47 Grassmann–Casimir Formalism (corrected)](https://github.com/nicholaskouns-create/E47-Kartekeya/blob/main/research/e47/E47_Grassmann_Casimir_Formalism_Corrected_20261008.md). It preserves the locked selector while correcting three possible conflations: the projector is self-adjoint in the physical `G` metric (`P^T G = G P`), `dim ker K = 47` while the distinct rank-43 Grassmann constraint map has `dim ker A = 82`, and `dim(E ∩ ker A)=47` does not imply set equality without an explicit witness.

Cross-platform route: [Notion canonical formalism](https://app.notion.com/p/3a046094fd30811eb015e14e1c5bce7c) · [Drive archive](https://docs.google.com/document/d/1F6UvhIOElXLoTPMW3VtOntxv86r81uKQeGcQikNv3bE) · [Supabase Citadel](https://gpkjvihkyectnenvnbng.supabase.co/functions/v1/city-app-host/see/) · [Linear REC-12](https://linear.app/4521/issue/REC-12/publish-e47-grassmann-casimir-proof-and-34-check-python-package).

Exact executable supplements: [SymPy witness](https://github.com/nicholaskouns-create/E47-Kartekeya/blob/main/research/e47/validation/e47_grassmann_casimir_witness_20261008.py) · [125-state simulation](https://github.com/nicholaskouns-create/E47-Kartekeya/blob/main/research/e47/validation/e47_grassmann_casimir_quantum_sim_20261008.py).

## Lock

```text
[LOCK] PASS  dimH=125  dimE47=47  rankK=78  Omega_c=47/125  Delta=11664  kappa=16  rho=15/17  TrP47=47
```

## Proof

Read [PROOF.md](PROOF.md). The repository keeps the Foundry lifetime algebra and the minimal E47 spectral engine needed to reproduce the intersection.

One line: **same split 47/78, different generator.** The Foundry fixture is built with the 47/78 split; the validator certifies that stamping, inheritance, and override carry it exactly. A fixture built with any other split comes back with that split.

## Executable surface

| File | Role |
|---|---|
| [python/spectral_engine.py](python/spectral_engine.py) | locked seven-sector E47 spectral engine |
| [python/data_lifetime_algebra.py](python/data_lifetime_algebra.py) | Foundry stamp / inherit / override algebra |
| [python/intersectionality_validator.py](python/intersectionality_validator.py) | repository-native 38-check E47 × Foundry validator |

The prior validator depended on external `/home/workdir/.grok/...` helper paths. The committed validator is self-contained apart from NumPy and the two files above.

## Run

```bash
python3 -m pip install -r python/REQUIREMENTS.txt
python3 python/spectral_engine.py
python3 python/data_lifetime_algebra.py
python3 python/intersectionality_validator.py
```

Expected terminal result:

```text
[INTERSECTIONALITY VALIDATOR] PASS  38/38 intersections hold
```

CI runs this exact route on every push and pull request.

## Related repositories

- [E47-Kartekeya](https://github.com/nicholaskouns-create/E47-Kartekeya) — canonical kernel, certificates, City runtime.
- [E47-Electroweak-Identities](https://github.com/nicholaskouns-create/E47-Electroweak-Identities) — electroweak identity instrument sharing the same locked kernel.
- [nicholaskouns-create.github.io](https://github.com/nicholaskouns-create/nicholaskouns-create.github.io) — public vestibule/router.