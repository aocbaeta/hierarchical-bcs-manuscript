"""Finite reduced-BCS model utilities.

Mode convention for level j:
    2*j     -> k_j up
    2*j + 1 -> -k_j down

The model is
    H = sum_j xi_j (n_{j up} + n_{j down})
        - g sum_{j,l} c^dag_{j up} c^dag_{j down} c_{l down} c_{l up}
        - eta sum_j (P_j^dag + P_j).

This file intentionally uses only numpy/scipy so the benchmark layer can run
even when Qiskit, Cirq, and PennyLane are not installed.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import reduce
from typing import Iterable

import numpy as np


I2 = np.eye(2, dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)
C = np.array([[0, 1], [0, 0]], dtype=complex)
CDAG = np.array([[0, 0], [1, 0]], dtype=complex)
N = CDAG @ C


@dataclass(frozen=True)
class BCSModel:
    xi: np.ndarray
    g: float
    eta: float = 0.0

    @property
    def n_levels(self) -> int:
        return int(len(self.xi))

    @property
    def n_modes(self) -> int:
        return 2 * self.n_levels

    @property
    def dim(self) -> int:
        return 2**self.n_modes


def kron_all(ops: Iterable[np.ndarray]) -> np.ndarray:
    return reduce(np.kron, ops)


def jw_annihilation(mode: int, n_modes: int) -> np.ndarray:
    ops = []
    for q in range(n_modes):
        if q < mode:
            ops.append(Z)
        elif q == mode:
            ops.append(C)
        else:
            ops.append(I2)
    return kron_all(ops)


def jw_creation(mode: int, n_modes: int) -> np.ndarray:
    return jw_annihilation(mode, n_modes).conj().T


def number(mode: int, n_modes: int) -> np.ndarray:
    return jw_creation(mode, n_modes) @ jw_annihilation(mode, n_modes)


def pair_annihilation(level: int, n_modes: int) -> np.ndarray:
    up = 2 * level
    dn = 2 * level + 1
    return jw_annihilation(dn, n_modes) @ jw_annihilation(up, n_modes)


def pair_creation(level: int, n_modes: int) -> np.ndarray:
    return pair_annihilation(level, n_modes).conj().T


def hamiltonian_matrix(model: BCSModel) -> np.ndarray:
    h = np.zeros((model.dim, model.dim), dtype=complex)
    for j, xi_j in enumerate(model.xi):
        h += xi_j * (number(2 * j, model.n_modes) + number(2 * j + 1, model.n_modes))
    for j in range(model.n_levels):
        pj_dag = pair_creation(j, model.n_modes)
        for l in range(model.n_levels):
            h += -model.g * pj_dag @ pair_annihilation(l, model.n_modes)
    if model.eta:
        for j in range(model.n_levels):
            p = pair_annihilation(j, model.n_modes)
            h += -model.eta * (p.conj().T + p)
    return 0.5 * (h + h.conj().T)


def exact_ground_state(model: BCSModel) -> dict:
    h = hamiltonian_matrix(model)
    evals, evecs = np.linalg.eigh(h)
    psi0 = evecs[:, 0]
    return {
        "energy": float(np.real(evals[0])),
        "eigenvalues": np.real(evals),
        "state": psi0,
        "hamiltonian": h,
    }


def pair_correlators(model: BCSModel, state: np.ndarray) -> np.ndarray:
    vals = []
    for j in range(model.n_levels):
        p = pair_annihilation(j, model.n_modes)
        vals.append(np.vdot(state, p @ state))
    return np.array(vals, dtype=complex)


def pair_correlation_matrix(model: BCSModel, state: np.ndarray) -> np.ndarray:
    corr = np.zeros((model.n_levels, model.n_levels), dtype=complex)
    pairs = [pair_annihilation(j, model.n_modes) for j in range(model.n_levels)]
    for j in range(model.n_levels):
        for l in range(model.n_levels):
            corr[j, l] = np.vdot(state, pairs[j].conj().T @ pairs[l] @ state)
    return 0.5 * (corr + corr.conj().T)


def gap_from_correlators(model: BCSModel, correlators: np.ndarray) -> complex:
    return model.g * np.sum(correlators)


def bcs_gap_iteration(model: BCSModel, beta: float = 1e6, tol: float = 1e-12, max_iter: int = 10000) -> dict:
    """Solve the uniform-coupling finite BCS gap equation.

    For constant attractive g, Delta = g sum_j Delta/(2 E_j) tanh(beta E_j/2).
    """
    delta = max(model.g, 1e-6)
    for iteration in range(max_iter):
        e = np.sqrt(model.xi**2 + abs(delta) ** 2)
        rhs = model.g * np.sum(delta / (2.0 * e) * np.tanh(0.5 * beta * e))
        mixed = 0.5 * delta + 0.5 * rhs
        if abs(mixed - delta) < tol:
            delta = mixed
            break
        delta = mixed

    e = np.sqrt(model.xi**2 + abs(delta) ** 2)
    u2 = 0.5 * (1.0 + model.xi / e)
    v2 = 0.5 * (1.0 - model.xi / e)
    anomalous = delta / (2.0 * e) * np.tanh(0.5 * beta * e)
    energy_mf = float(np.sum(2.0 * model.xi * v2) - abs(delta) ** 2 / model.g)
    return {
        "delta": float(np.real(delta)),
        "quasiparticle_energies": e,
        "u2": u2,
        "v2": v2,
        "anomalous": anomalous,
        "energy_mean_field": energy_mf,
        "iterations": iteration + 1,
    }


def hierarchy_residual(model: BCSModel, state: np.ndarray) -> dict:
    """A small diagnostic for pair-sector closure quality.

    In an exactly diagonalized finite Hamiltonian with particle-number
    conservation, <P_j> vanishes unless an explicit symmetry-breaking field is
    added. The stable finite-size diagnostic is therefore the pair-density
    matrix C_{jl}=<P_j^dag P_l>. We compare it with the rank-one matrix
    generated by the BCS projected anomalous profile.
    """
    exact_phi = pair_correlators(model, state)
    pair_density = pair_correlation_matrix(model, state)
    evals, evecs = np.linalg.eigh(pair_density)
    leading_profile = evecs[:, int(np.argmax(evals))]

    closure = bcs_gap_iteration(model)
    projected_phi = np.asarray(closure["anomalous"], dtype=complex)
    projected_density = np.outer(projected_phi.conj(), projected_phi)
    denom_proj = np.vdot(projected_density, projected_density)
    if abs(denom_proj) > 1e-14:
        scale = np.vdot(projected_density, pair_density) / denom_proj
        projected_density = scale * projected_density

    numerator = np.linalg.norm(pair_density - projected_density)
    denominator = max(np.linalg.norm(pair_density), 1e-14)
    return {
        "exact_pair_amplitudes": exact_phi,
        "exact_pair_density": pair_density,
        "leading_pair_density_eigenvalue": float(np.max(np.real(evals))),
        "leading_pair_profile": leading_profile,
        "projected_pair_amplitudes": projected_phi,
        "relative_pair_density_residual": float(numerator / denominator),
    }


def source_response(model: BCSModel, state: np.ndarray) -> dict:
    """Number-symmetry-breaking response induced by the external pair source."""
    phi = pair_correlators(model, state)
    closure = bcs_gap_iteration(BCSModel(xi=model.xi, g=model.g, eta=0.0))
    projected_phi = np.asarray(closure["anomalous"], dtype=complex)
    denom = max(np.linalg.norm(projected_phi), 1e-14)
    phase_aligned_phi = phi
    if np.linalg.norm(phi) > 1e-14:
        phase = np.vdot(projected_phi, phi)
        if abs(phase) > 1e-14:
            phase_aligned_phi = phi * np.exp(-1j * np.angle(phase))
    source_error = np.linalg.norm(phase_aligned_phi - projected_phi) / denom
    return {
        "source_pair_amplitudes": phi,
        "source_pair_norm": float(np.linalg.norm(phi)),
        "bcs_pair_norm": float(np.linalg.norm(projected_phi)),
        "relative_source_profile_error": float(source_error),
    }


def default_model(n_levels: int = 4, g: float = 0.7, eta: float = 0.0) -> BCSModel:
    xi = np.linspace(-1.5, 1.5, n_levels)
    return BCSModel(xi=xi, g=g, eta=eta)
