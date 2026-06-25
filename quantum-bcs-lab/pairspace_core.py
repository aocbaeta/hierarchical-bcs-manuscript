"""Pair-subspace representation of the finite reduced BCS Hamiltonian.

The reduced BCS Hamiltonian preserves the subspace in which each level is either
empty or occupied by a complete time-reversed pair. The source term
    - eta sum_j (P_j^dag + P_j)
also stays inside this pair subspace. This representation has dimension 2**N
instead of 2**(2*N), enabling larger scaling sweeps.
"""

from __future__ import annotations

import numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import eigsh

from bcs_core import BCSModel, bcs_gap_iteration


def pairspace_hamiltonian(model: BCSModel) -> np.ndarray:
    dim = 2**model.n_levels
    h = np.zeros((dim, dim), dtype=complex)

    for state in range(dim):
        occupied = [(state >> j) & 1 for j in range(model.n_levels)]
        h[state, state] += sum(2.0 * model.xi[j] * occupied[j] for j in range(model.n_levels))

        for j in range(model.n_levels):
            if occupied[j]:
                h[state, state] += -model.g

        for l in range(model.n_levels):
            if not occupied[l]:
                continue
            removed = state & ~(1 << l)
            for j in range(model.n_levels):
                if (removed >> j) & 1:
                    continue
                target = removed | (1 << j)
                if target != state:
                    h[target, state] += -model.g

        if abs(model.eta):
            for j in range(model.n_levels):
                if (state >> j) & 1:
                    target = state & ~(1 << j)
                    h[target, state] += -np.conj(model.eta)
                else:
                    target = state | (1 << j)
                    h[target, state] += -model.eta

    return 0.5 * (h + h.conj().T)


def pairspace_hamiltonian_sparse(model: BCSModel) -> coo_matrix:
    dim = 2**model.n_levels
    rows = []
    cols = []
    data = []

    for state in range(dim):
        occupied = [(state >> j) & 1 for j in range(model.n_levels)]
        diagonal = sum(2.0 * model.xi[j] * occupied[j] for j in range(model.n_levels))
        diagonal += sum(-model.g for j in range(model.n_levels) if occupied[j])
        rows.append(state)
        cols.append(state)
        data.append(diagonal)

        for l in range(model.n_levels):
            if not occupied[l]:
                continue
            removed = state & ~(1 << l)
            for j in range(model.n_levels):
                if (removed >> j) & 1:
                    continue
                target = removed | (1 << j)
                if target != state:
                    rows.append(target)
                    cols.append(state)
                    data.append(-model.g)

        if abs(model.eta):
            for j in range(model.n_levels):
                if (state >> j) & 1:
                    target = state & ~(1 << j)
                    value = -np.conj(model.eta)
                else:
                    target = state | (1 << j)
                    value = -model.eta
                rows.append(target)
                cols.append(state)
                data.append(value)

    h = coo_matrix((data, (rows, cols)), shape=(dim, dim), dtype=complex).tocsr()
    return 0.5 * (h + h.getH())


def exact_pairspace_ground_state(model: BCSModel) -> dict:
    h = pairspace_hamiltonian(model)
    evals, evecs = np.linalg.eigh(h)
    return {
        "energy": float(np.real(evals[0])),
        "eigenvalues": np.real(evals),
        "state": evecs[:, 0],
        "hamiltonian": h,
    }


def exact_pairspace_ground_state_sparse(model: BCSModel) -> dict:
    h = pairspace_hamiltonian_sparse(model)
    evals, evecs = eigsh(h, k=1, which="SA", tol=1e-10, maxiter=max(1000, 20 * h.shape[0]))
    state = evecs[:, 0]
    return {
        "energy": float(np.real(evals[0])),
        "state": state,
        "hamiltonian_shape": h.shape,
        "hamiltonian_nnz": int(h.nnz),
    }


def pairspace_pair_amplitudes(model: BCSModel, state: np.ndarray) -> np.ndarray:
    vals = np.zeros(model.n_levels, dtype=complex)
    dim = len(state)
    for basis in range(dim):
        amp = state[basis]
        if abs(amp) < 1e-15:
            continue
        for j in range(model.n_levels):
            if (basis >> j) & 1:
                target = basis & ~(1 << j)
                vals[j] += np.conj(state[target]) * amp
    return vals


def pairspace_pair_density(model: BCSModel, state: np.ndarray) -> np.ndarray:
    corr = np.zeros((model.n_levels, model.n_levels), dtype=complex)
    dim = len(state)
    for basis in range(dim):
        amp = state[basis]
        if abs(amp) < 1e-15:
            continue
        for l in range(model.n_levels):
            if not ((basis >> l) & 1):
                continue
            removed = basis & ~(1 << l)
            for j in range(model.n_levels):
                if (removed >> j) & 1:
                    continue
                target = removed | (1 << j)
                corr[j, l] += np.conj(state[target]) * amp
    return 0.5 * (corr + corr.conj().T)


def pairspace_source_response(model: BCSModel, state: np.ndarray) -> dict:
    phi = pairspace_pair_amplitudes(model, state)
    closure = bcs_gap_iteration(BCSModel(xi=model.xi, g=model.g, eta=0.0))
    projected_phi = np.asarray(closure["anomalous"], dtype=complex)
    denom = max(np.linalg.norm(projected_phi), 1e-14)
    phase_aligned_phi = phi
    if np.linalg.norm(phi) > 1e-14:
        phase = np.vdot(projected_phi, phi)
        if abs(phase) > 1e-14:
            phase_aligned_phi = phi * np.exp(-1j * np.angle(phase))
    return {
        "source_pair_amplitudes": phi,
        "source_pair_norm": float(np.linalg.norm(phi)),
        "source_pair_phase": float(np.angle(np.sum(phi))) if np.linalg.norm(phi) > 1e-14 else 0.0,
        "eta_phase": float(np.angle(model.eta)) if abs(model.eta) > 1e-14 else 0.0,
        "bcs_pair_norm": float(np.linalg.norm(projected_phi)),
        "relative_source_profile_error": float(np.linalg.norm(phase_aligned_phi - projected_phi) / denom),
    }


def pairspace_density_residual(model: BCSModel, state: np.ndarray) -> dict:
    pair_density = pairspace_pair_density(model, state)
    evals = np.linalg.eigvalsh(pair_density)
    closure = bcs_gap_iteration(BCSModel(xi=model.xi, g=model.g, eta=0.0))
    projected_phi = np.asarray(closure["anomalous"], dtype=complex)
    projected_density = np.outer(projected_phi.conj(), projected_phi)
    denom_proj = np.vdot(projected_density, projected_density)
    if abs(denom_proj) > 1e-14:
        projected_density = (np.vdot(projected_density, pair_density) / denom_proj) * projected_density
    return {
        "leading_pair_density_eigenvalue": float(np.max(np.real(evals))),
        "relative_pair_density_residual": float(
            np.linalg.norm(pair_density - projected_density) / max(np.linalg.norm(pair_density), 1e-14)
        ),
    }
