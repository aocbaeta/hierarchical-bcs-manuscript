"""Cirq layer: construct the BCS PauliSum and run a tiny exact simulation."""

from __future__ import annotations

import numpy as np

from bcs_core import default_model, exact_ground_state
from pauli_mapper import bcs_pauli_terms


def main() -> None:
    try:
        import cirq
    except ImportError as exc:
        raise SystemExit("Cirq is not installed. Run: pip install cirq") from exc

    model = default_model(n_levels=3, g=0.7)
    qubits = cirq.LineQubit.range(model.n_modes)

    pauli_sum = 0
    for coeff, label in bcs_pauli_terms(model):
        term = complex(coeff)
        for q, ch in enumerate(label):
            if ch == "X":
                term *= cirq.X(qubits[q])
            elif ch == "Y":
                term *= cirq.Y(qubits[q])
            elif ch == "Z":
                term *= cirq.Z(qubits[q])
        pauli_sum += term

    circuit = cirq.Circuit()
    # Prepare a simple pair-product trial state for dynamics diagnostics.
    for j in range(model.n_levels):
        circuit.append(cirq.ry(np.pi / 2).on(qubits[2 * j]))
        circuit.append(cirq.CNOT(qubits[2 * j], qubits[2 * j + 1]))

    simulator = cirq.Simulator()
    state = simulator.simulate(circuit).final_state_vector
    energy = pauli_sum.expectation_from_state_vector(state, qubit_map={q: i for i, q in enumerate(qubits)})
    exact = exact_ground_state(model)

    print("Cirq finite BCS PauliSum benchmark")
    print(f"qubits: {model.n_modes}")
    print(f"trial pair-state energy: {float(np.real(energy)):.12f}")
    print(f"exact ground energy: {exact['energy']:.12f}")
    print(f"Pauli terms: {len(bcs_pauli_terms(model))}")


if __name__ == "__main__":
    main()
