"""PennyLane layer: differentiable BCS-pair VQE ansatz."""

from __future__ import annotations

import numpy as np

from bcs_core import default_model, exact_ground_state
from pauli_mapper import bcs_pauli_terms


def main() -> None:
    try:
        import pennylane as qml
        from pennylane import numpy as pnp
    except ImportError as exc:
        raise SystemExit("PennyLane is not installed. Run: pip install pennylane") from exc

    model = default_model()
    terms = bcs_pauli_terms(model)
    coeffs = [float(np.real(c)) for c, _ in terms]

    def obs_from_label(label: str):
        factors = []
        for wire, ch in enumerate(label):
            if ch == "X":
                factors.append(qml.PauliX(wire))
            elif ch == "Y":
                factors.append(qml.PauliY(wire))
            elif ch == "Z":
                factors.append(qml.PauliZ(wire))
        if not factors:
            return qml.Identity(0)
        return factors[0] if len(factors) == 1 else qml.prod(*factors)

    hamiltonian = qml.Hamiltonian(coeffs, [obs_from_label(label) for _, label in terms])
    dev = qml.device("default.qubit", wires=model.n_modes)

    @qml.qnode(dev)
    def energy(theta):
        # Pair-product BCS ansatz: cos(theta_j/2)|00> + sin(theta_j/2)|11>.
        for j in range(model.n_levels):
            up = 2 * j
            dn = 2 * j + 1
            qml.RY(theta[j], wires=up)
            qml.CNOT(wires=[up, dn])
        return qml.expval(hamiltonian)

    theta = pnp.array([np.pi / 2] * model.n_levels, requires_grad=True)
    opt = qml.AdamOptimizer(stepsize=0.08)
    for _ in range(250):
        theta = opt.step(energy, theta)

    exact = exact_ground_state(model)
    print("PennyLane BCS-pair VQE benchmark")
    print(f"qubits: {model.n_modes}")
    print(f"VQE energy: {float(energy(theta)):.12f}")
    print(f"exact ground energy: {exact['energy']:.12f}")
    print("theta:", np.array(theta).round(6))


if __name__ == "__main__":
    main()
