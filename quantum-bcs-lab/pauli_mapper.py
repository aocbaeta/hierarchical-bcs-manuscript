"""Jordan-Wigner Pauli-string mapper shared by Qiskit, PennyLane, and Cirq."""

from __future__ import annotations

from collections import defaultdict
from typing import Iterable

import numpy as np

from bcs_core import BCSModel


SingleTerm = tuple[complex, str]


_MUL = {
    ("I", "I"): (1, "I"),
    ("I", "X"): (1, "X"),
    ("I", "Y"): (1, "Y"),
    ("I", "Z"): (1, "Z"),
    ("X", "I"): (1, "X"),
    ("Y", "I"): (1, "Y"),
    ("Z", "I"): (1, "Z"),
    ("X", "X"): (1, "I"),
    ("Y", "Y"): (1, "I"),
    ("Z", "Z"): (1, "I"),
    ("X", "Y"): (1j, "Z"),
    ("Y", "X"): (-1j, "Z"),
    ("Y", "Z"): (1j, "X"),
    ("Z", "Y"): (-1j, "X"),
    ("Z", "X"): (1j, "Y"),
    ("X", "Z"): (-1j, "Y"),
}


def multiply_strings(a: SingleTerm, b: SingleTerm) -> SingleTerm:
    coeff_a, str_a = a
    coeff_b, str_b = b
    coeff = coeff_a * coeff_b
    out = []
    for pa, pb in zip(str_a, str_b):
        phase, pc = _MUL[(pa, pb)]
        coeff *= phase
        out.append(pc)
    return coeff, "".join(out)


def multiply_expansions(left: Iterable[SingleTerm], right: Iterable[SingleTerm]) -> list[SingleTerm]:
    acc = defaultdict(complex)
    for a in left:
        for b in right:
            coeff, label = multiply_strings(a, b)
            acc[label] += coeff
    return [(coeff, label) for label, coeff in acc.items() if abs(coeff) > 1e-12]


def jw_single(mode: int, n_modes: int, dagger: bool) -> list[SingleTerm]:
    z_prefix = ["Z" if q < mode else "I" for q in range(n_modes)]
    x = z_prefix.copy()
    y = z_prefix.copy()
    x[mode] = "X"
    y[mode] = "Y"
    sign = -1j if dagger else 1j
    return [(0.5, "".join(x)), (0.5 * sign, "".join(y))]


def jw_product(ops: list[tuple[str, int]], n_modes: int) -> list[SingleTerm]:
    expansion = [(1.0 + 0j, "I" * n_modes)]
    for kind, mode in ops:
        expansion = multiply_expansions(expansion, jw_single(mode, n_modes, dagger=(kind == "create")))
    return expansion


def bcs_pauli_terms(model: BCSModel) -> list[SingleTerm]:
    acc = defaultdict(complex)

    for j, xi_j in enumerate(model.xi):
        for mode in [2 * j, 2 * j + 1]:
            # n = (I - Z)/2 in this convention.
            ident = "I" * model.n_modes
            z = list(ident)
            z[mode] = "Z"
            acc[ident] += 0.5 * xi_j
            acc["".join(z)] += -0.5 * xi_j

    for j in range(model.n_levels):
        for l in range(model.n_levels):
            ops = [
                ("create", 2 * j),
                ("create", 2 * j + 1),
                ("destroy", 2 * l + 1),
                ("destroy", 2 * l),
            ]
            for coeff, label in jw_product(ops, model.n_modes):
                acc[label] += -model.g * coeff

    terms = [(coeff, label) for label, coeff in acc.items() if abs(coeff) > 1e-10]
    terms.sort(key=lambda item: item[1])
    return terms


def pauli_matrix(label: str) -> np.ndarray:
    mats = {
        "I": np.eye(2, dtype=complex),
        "X": np.array([[0, 1], [1, 0]], dtype=complex),
        "Y": np.array([[0, -1j], [1j, 0]], dtype=complex),
        "Z": np.array([[1, 0], [0, -1]], dtype=complex),
    }
    out = mats[label[0]]
    for ch in label[1:]:
        out = np.kron(out, mats[ch])
    return out


def pauli_matrix_sum(terms: list[SingleTerm]) -> np.ndarray:
    dim = 2 ** len(terms[0][1])
    h = np.zeros((dim, dim), dtype=complex)
    for coeff, label in terms:
        h += coeff * pauli_matrix(label)
    return 0.5 * (h + h.conj().T)
