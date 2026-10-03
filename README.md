# FOUNDRY-LIFETIME-E47-INTERSECTION

> **Main entry portal:** [The Mathematical City](https://nicholaskouns-create.github.io/website/) — explore the districts, interactive labs, and research index.
>
> **[Explore PiP Manta](https://nicholaskouns-create.github.io/E47-Kartekeya/interfaces/pip-manta/embed.html)**


**Mark:** Foundry Data Lifetime algebra run through the locked E47 kernel.  
**Owner:** Nicholas Kouns (`nicholaskouns-create`)  
**Kernel authority:** [E47-Kartekeya](https://github.com/nicholaskouns-create/E47-Kartekeya)

`K=(C-6I)(C-30I)`, `dim H=125`, `dim E47=47`, `Omega_c=47/125`.

## Lock

```text
[LOCK] PASS  dimH=125  dimE47=47  rankK=78  Omega_c=47/125  Delta=11664  kappa=16  rho=15/17  TrP47=47
```

## Proof

Read [PROOF.md](PROOF.md). The repository keeps the Foundry lifetime algebra and the minimal E47 spectral engine needed to reproduce the intersection.

One line: **same split 47/78, different generator.**

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
