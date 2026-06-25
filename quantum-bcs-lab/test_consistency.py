"""Lightweight consistency checks for the BCS quantum lab."""

from __future__ import annotations

import numpy as np

from bcs_core import default_model, exact_ground_state, source_response
from pairspace_core import exact_pairspace_ground_state, pairspace_source_response
from pauli_mapper import bcs_pauli_terms, pauli_matrix_sum


def assert_close(name: str, value: float, threshold: float) -> None:
    if value > threshold:
        raise AssertionError(f"{name}={value:.3e} exceeds threshold {threshold:.3e}")


def main() -> None:
    zero_source = default_model(n_levels=4, g=0.7, eta=0.0)
    full_zero = exact_ground_state(zero_source)
    zero_response = source_response(zero_source, full_zero["state"])
    assert_close("zero-source anomalous norm", zero_response["source_pair_norm"], 1e-10)

    sourced = default_model(n_levels=4, g=0.7, eta=0.01)
    full = exact_ground_state(sourced)
    pair = exact_pairspace_ground_state(sourced)
    assert_close("full-vs-pairspace ground energy", abs(full["energy"] - pair["energy"]), 1e-10)

    full_source = source_response(sourced, full["state"])
    pair_source = pairspace_source_response(sourced, pair["state"])
    assert_close(
        "full-vs-pairspace source norm",
        abs(full_source["source_pair_norm"] - pair_source["source_pair_norm"]),
        1e-10,
    )
    if pair_source["source_pair_norm"] <= 1e-6:
        raise AssertionError("source anomalous norm did not become nonzero")

    mapped_h = pauli_matrix_sum(bcs_pauli_terms(sourced))
    assert_close("Jordan-Wigner matrix error", float(np.linalg.norm(mapped_h - full["hamiltonian"])), 1e-10)
    print("All consistency checks passed.")


if __name__ == "__main__":
    main()
