# MARK: FOUNDRY-LIFETIME-E47-INTERSECTION / E47-ENGINE
# Kernel lock: dimH=125 dimE47=47 rankK=78 Omega_c=47/125
#!/usr/bin/env python3
"""KKP-R SPECTRAL ENGINE — H=V2**3 dim=125, K=(C-6I)(C-30I), ker=E47."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, Tuple
import numpy as np

J_PRIMITIVE: int = 2
D_PRIMITIVE: int = 2 * J_PRIMITIVE + 1
DIM_H: int = D_PRIMITIVE ** 3
SPINS = np.array([0, 1, 2, 3, 4, 5, 6], dtype=int)
MULTIPLICITIES = np.array([1, 3, 5, 4, 3, 2, 1], dtype=int)
SECTOR_DIMS_LOCKED = np.array([1, 9, 25, 28, 27, 22, 13], dtype=int)
CASIMIR_LOCKED = np.array([0, 2, 6, 12, 20, 30, 42], dtype=int)
MU_LOCKED = np.array([180, 112, 0, -108, -140, 0, 432], dtype=int)
MU2_LOCKED = np.array([32400, 12544, 0, 11664, 19600, 0, 186624], dtype=int)
DIM_KERNEL_LOCKED: int = 47
DIM_COMPLEMENT_LOCKED: int = 78
OMEGA_C_LOCKED: float = 47 / 125
R_MARGIN_LOCKED: float = 78 / 47
SPECTRAL_GAP_LOCKED: int = 11664
LAMBDA_MAX_LOCKED: int = 186624
KAPPA_LOCKED: int = 16
RHO_LOCKED: float = 15 / 17
P47_NORMALIZER: float = 1_814_400.0
P47_ON_SPEC_LOCKED = np.array([0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0])

def P_47(C):
    C = np.asarray(C, dtype=float)
    return (C - 31.0) * C * (C - 2.0) * (C - 12.0) * (C - 20.0) * (C - 42.0) / P47_NORMALIZER

@dataclass(frozen=True)
class SpectralEngine:
    spins: np.ndarray = field(default_factory=lambda: SPINS.copy())
    multiplicities: np.ndarray = field(default_factory=lambda: MULTIPLICITIES.copy())
    def __post_init__(self) -> None:
        object.__setattr__(self, "spins", np.asarray(self.spins, dtype=int))
        object.__setattr__(self, "multiplicities", np.asarray(self.multiplicities, dtype=int))
        self.validate()
    @property
    def subspace_dims(self) -> np.ndarray:
        return 2 * self.spins + 1
    @property
    def sector_dims(self) -> np.ndarray:
        return self.multiplicities * self.subspace_dims
    @property
    def dim_H(self) -> int:
        return int(np.sum(self.sector_dims))
    @property
    def casimir(self) -> np.ndarray:
        return self.spins * (self.spins + 1)
    @property
    def mu(self) -> np.ndarray:
        lam = self.casimir
        return (lam - 6) * (lam - 30)
    @property
    def mu2(self) -> np.ndarray:
        return self.mu ** 2
    @property
    def kernel_mask(self) -> np.ndarray:
        return self.mu == 0
    @property
    def dim_kernel(self) -> int:
        return int(np.sum(self.sector_dims[self.kernel_mask]))
    @property
    def dim_complement(self) -> int:
        return int(np.sum(self.sector_dims[~self.kernel_mask]))
    @property
    def omega_c(self) -> float:
        return self.dim_kernel / self.dim_H
    @property
    def r_margin(self) -> float:
        return self.dim_complement / self.dim_kernel
    @property
    def spectral_gap(self) -> int:
        return int(np.min(self.mu2[~self.kernel_mask]))
    @property
    def lambda_max(self) -> int:
        return int(np.max(self.mu2))
    @property
    def kappa(self) -> float:
        return self.lambda_max / self.spectral_gap
    @property
    def rho(self) -> float:
        return (self.kappa - 1.0) / (self.kappa + 1.0)
    @property
    def P_on_spectrum(self) -> np.ndarray:
        return P_47(self.casimir.astype(float))
    @property
    def trace_P47(self) -> float:
        return float(np.sum(self.sector_dims * self.P_on_spectrum))
    def table(self) -> Dict[str, np.ndarray]:
        return {"J": self.spins, "m_J": self.multiplicities, "d_J": self.subspace_dims, "dim": self.sector_dims, "lambda": self.casimir, "mu": self.mu, "mu2": self.mu2, "P47": self.P_on_spectrum, "kernel": self.kernel_mask.astype(int)}
    def report(self) -> str:
        return f"dim H={self.dim_H} dim E47={self.dim_kernel} rank K={self.dim_complement} Omega_c={self.omega_c} Delta={self.spectral_gap} kappa={self.kappa} rho={self.rho} TrP47={self.trace_P47}"
    def validate(self) -> None:
        assert DIM_H == 125 and self.dim_H == 125
        assert np.array_equal(self.sector_dims, SECTOR_DIMS_LOCKED)
        assert np.array_equal(self.casimir, CASIMIR_LOCKED)
        assert np.array_equal(self.mu, MU_LOCKED)
        assert np.array_equal(self.mu2, MU2_LOCKED)
        assert self.dim_kernel == 47 and self.dim_complement == 78
        assert self.omega_c == OMEGA_C_LOCKED
        assert self.spectral_gap == 11664 and self.lambda_max == 186624
        assert self.kappa == 16 and self.rho == RHO_LOCKED
        assert np.allclose(self.P_on_spectrum, P47_ON_SPEC_LOCKED)
        assert np.isclose(self.trace_P47, 47.0)

def run_engine() -> SpectralEngine:
    eng = SpectralEngine()
    print("[LOCK] PASS  dimH=125  dimE47=47  rankK=78  Omega_c=47/125")
    print(eng.report())
    return eng

if __name__ == "__main__":
    run_engine()
