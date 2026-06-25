"""Run the finite-BCS benchmark with exact diagonalization and BCS closure."""

from __future__ import annotations

import argparse
import json

import numpy as np

from bcs_core import bcs_gap_iteration, default_model, exact_ground_state, hierarchy_residual
from pauli_mapper import bcs_pauli_terms, pauli_matrix_sum


def as_jsonable(obj):
    if isinstance(obj, np.ndarray):
        if np.iscomplexobj(obj):
            return [[float(np.real(x)), float(np.imag(x))] for x in obj.ravel()]
        return obj.tolist()
    if isinstance(obj, complex):
        return [float(np.real(obj)), float(np.imag(obj))]
    if isinstance(obj, np.generic):
        return obj.item()
    return obj


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--levels", type=int, default=4)
    parser.add_argument("--g", type=float, default=0.7)
    args = parser.parse_args()

    model = default_model(n_levels=args.levels, g=args.g)
    exact = exact_ground_state(model)
    closure = bcs_gap_iteration(model)
    residual = hierarchy_residual(model, exact["state"])

    terms = bcs_pauli_terms(model)
    mapped_h = pauli_matrix_sum(terms)
    mapping_error = float(np.linalg.norm(mapped_h - exact["hamiltonian"]))

    report = {
        "model": {
            "n_levels": model.n_levels,
            "n_qubits": model.n_modes,
            "xi": model.xi.tolist(),
            "g": model.g,
        },
        "exact_ground_energy": exact["energy"],
        "bcs_mean_field_energy": closure["energy_mean_field"],
        "bcs_gap_delta": closure["delta"],
        "leading_pair_density_eigenvalue": residual["leading_pair_density_eigenvalue"],
        "relative_pair_density_residual": residual["relative_pair_density_residual"],
        "pauli_terms": len(terms),
        "jw_mapping_matrix_error": mapping_error,
    }

    print(json.dumps(report, indent=2, default=as_jsonable))


if __name__ == "__main__":
    main()
