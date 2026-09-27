# First-Principles Proof Plate
## E47 Kernel ∩ Foundry Data Lifetime Algebra

**Mark:** `FOUNDRY-LIFETIME-E47-INTERSECTION`
**Author:** Nicholas Kouns / KKP-R
**Lock:** `[LOCK] PASS  dimH=125  dimE47=47  rankK=78  Omega_c=47/125  Delta=11664  kappa=16  rho=15/17  TrP47=47`
**Date:** 2026-09-27

Do not retune these numbers. They are not parameters.

## 0. Notation

- su(2) — compact simple Lie algebra
- V_J — irrep, dim = 2J+1, Casimir λ_J = J(J+1)
- H = V_2^{⊗ 3} — carrier, dim H = 125
- C — Casimir of the diagonal su(2) action on H
- K = (C-6I)(C-30I) — constraint kernel
- E_47 = ker K = E_6 ⊕ E_30 — kernel, dim 25+22 = 47
- P_47(C) — Lagrange projector onto E_47
- D, τ, b, V(D,b) — Foundry dataset, transaction, branch, latest view
- δ(τ) ∈ Time ∪ {⊥} — Lifetime deletion date (⊥ = keep)
- G — provenance DAG on transactions
- π_*G — push of δ along parent→child

## 1. Representation theorem (carrier)

Axiom. Finite-dimensional representations of su(2) are completely reducible.

Primitive. Take V_2, dim = 5.

Carrier.

    H = V_2 ⊗ V_2 ⊗ V_2,    dim H = 5^3 = 125.

CG range. Three integer spin-2 factors produce only J = 0,…,6.

Locked multiplicities.

    m_J = (1, 3, 5, 4, 3, 2, 1).

Isotypic dimensions.

    m_J (2J+1) = (1, 9, 25, 28, 27, 22, 13),    sum = 125.

Casimir spectrum.

    λ_J = J(J+1) = (0, 2, 6, 12, 20, 30, 42).

Q.E.D. on the carrier. No free integer remains.

## 2. Kernel theorem

Any su(2)-equivariant endomorphism is block-scalar on isotypics (Schur). Polynomials in C are equivariant.

    K = (C - 6I)(C - 30I).

On V_J,

    μ_J = (λ_J - 6)(λ_J - 30) = (180, 112, 0, -108, -140, 0, 432).

Zeros exactly at J=2 and J=5:

    ker K = E_6 ⊕ E_30.

Intersection of kernel isotypics: E_6 ∩ E_30 = {0}.

Join: dim E_47 = 25+22 = 47, rank K = 78.

Threshold: Ω_c = 47/125 = 0.376.

Q.E.D. on the split.

## 3. Projector theorem

Lagrange interpolant on spec(C) with value 1 on {6,30} and 0 on the rest:

    P_47(C) = C(C-2)(C-12)(C-20)(C-31)(C-42) / 1814400.

Then P_47 |_{ker K} = I, P_47 |_{perp} = 0, Tr P_47 = 47,
and P_47 (I-P_47) = 0 on spec(C).

Q.E.D. on complementarity of keep/drop.

## 4. Dynamics theorem (E47 generator)

    ρ̇ = -K² ρ,    σ(K²) = μ_J²
    σ(K²) = (32400, 12544, 0, 11664, 19600, 0, 186624).

Gap at J=3: Δ = 11664. Stiff at J=6: Λ_max = 186624.

    κ = Λ_max / Δ = 16,    ρ_disc = (κ-1)/(κ+1) = 15/17.

Kernel is invariant: K² P_47 = 0. Complement contracts in place on H. No copy off the module.

Q.E.D. on the E47 generator.

## 5. Foundry Lifetime algebra

Objects. Transactions τ on datasets D, branches b, views V(D,b) obtained by folding SNAPSHOT / APPEND / UPDATE / DELETE.

Fixed date π = (T, C):

    δ_fix(τ) = T  if C=⊥ or t(τ)<C;  ⊥ if t(τ)≥C.

Latest-view-only π = B_π:

    L(τ) = {b ∈ B_π : τ ∈ V(D,b)}
    δ_LVO(τ) = ⊥ if L(τ)≠∅;
                 t(τ_newest) if L=∅ and b∈B_π;
                 t(τ) if b∉B_π.

Inheritance:

    δ(τ) = min{δ(p) : p ∈ P(τ), δ(p)≠⊥}
    (⊥ if every parent is ⊥).

Seeds (policy-attached datasets) are not overwritten by their parents.

Override. Cut δ on D ∪ Desc(D). Optional reseed π'.

Retention. Local mark. No Desc walk.

Q.E.D. on the Foundry generator π_*G.

## 6. Intersection theorem

Construct a raw dataset with 125 transactions, live view size 47, complement 78, and one derived child per transaction. Then

    |V(D,b)| = 47 = dim E_47
    |V^c| = 78 = rank K
    ω-hat = |V|/|D| = 47/125 = Ω_c
    V ∩ V^c = ∅ = E_47 ∩ E_47^perp
    Ret ⊂ DL,  |DL \ Ret| = 78 = cascade
    override(D_derived) ∩ {τ : δ(τ)≠⊥ and τ ∈ Desc} = ∅

Validated: python/intersectionality_validator.py — 38/38 PASS.

Same split 47/78. Different generator.

    K² ∈ End_su(2)(H)   contracts a field in place
    π_*G                 copies a date along a DAG

Q.E.D.
