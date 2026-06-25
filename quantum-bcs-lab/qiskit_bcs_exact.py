"""Qiskit layer: build the finite BCS Hamiltonian as a SparsePauliOp."""

from __future__ import annotations

import numpy as np

from bcs_core import default_model, exact_ground_state
from pauli_mapper import bcs_pauli_terms


def main() -> None:
    try:
        from qiskit.quantum_info import SparsePauliOp
    except ImportError as exc:
        raise SystemExit("Qiskit is not installed. Run: pip install qiskit") from exc

    model = default_model()
    terms = bcs_pauli_terms(model)
    op = SparsePauliOp.from_list([(label, coeff) for coeff, label in terms])
    dense = op.to_matrix()
    exact = exact_ground_state(model)
    evals = np.linalg.eigvalsh(dense)

    print("Qiskit SparsePauliOp finite BCS benchmark")
    print(f"qubits: {model.n_modes}")
    print(f"Pauli terms: {len(terms)}")
    print(f"ground energy from Qiskit matrix: {float(np.real(evals[0])):.12f}")
    print(f"ground energy from core exact ED: {exact['energy']:.12f}")


if __name__ == "__main__":
    main()
