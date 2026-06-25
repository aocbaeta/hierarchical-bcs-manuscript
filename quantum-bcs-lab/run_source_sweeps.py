"""Pair-source sweeps for finite BCS models.

The source term
    - eta sum_j (P_j^dag + P_j)
breaks particle-number symmetry explicitly. This makes <P_j> nonzero in exact
diagonalization, allowing a direct finite-size comparison with the BCS
anomalous profile. The physically interesting limit is eta -> 0 after the
large-system trend is understood.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from bcs_core import bcs_gap_iteration, default_model, exact_ground_state, source_response
from pauli_mapper import bcs_pauli_terms, pauli_matrix_sum


def run_source_sweep(levels_values: list[int], eta_values: np.ndarray, g: float) -> list[dict]:
    rows: list[dict] = []
    for levels in levels_values:
        zero_source_model = default_model(n_levels=levels, g=g, eta=0.0)
        closure = bcs_gap_iteration(zero_source_model)
        for eta in eta_values:
            model = default_model(n_levels=levels, g=g, eta=float(eta))
            exact = exact_ground_state(model)
            source = source_response(model, exact["state"])
            mapped_h = pauli_matrix_sum(bcs_pauli_terms(model))
            mapping_error = float(np.linalg.norm(mapped_h - exact["hamiltonian"]))
            rows.append(
                {
                    "levels": levels,
                    "qubits": model.n_modes,
                    "g": g,
                    "eta": float(eta),
                    "exact_energy": exact["energy"],
                    "bcs_gap": closure["delta"],
                    "source_pair_norm": source["source_pair_norm"],
                    "source_pair_phase": source["source_pair_phase"],
                    "bcs_pair_norm": source["bcs_pair_norm"],
                    "relative_source_profile_error": source["relative_source_profile_error"],
                    "jw_mapping_matrix_error": mapping_error,
                }
            )
    return rows


def save_csv(rows: list[dict], path: Path) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def plot_source_sweeps(rows: list[dict], output_dir: Path) -> None:
    levels_values = sorted({row["levels"] for row in rows})

    def arr(levels: int, key: str) -> np.ndarray:
        subset = [row for row in rows if row["levels"] == levels]
        subset.sort(key=lambda item: item["eta"])
        return np.array([row[key] for row in subset], dtype=float)

    plots = [
        ("Pair-source eta", "||<P>_eta||", "source_pair_norm", "source_pair_norm_vs_eta.png"),
        (
            "Pair-source eta",
            "Relative source-profile error",
            "relative_source_profile_error",
            "source_profile_error_vs_eta.png",
        ),
        (
            "Pair-source eta",
            "JW mapping matrix error",
            "jw_mapping_matrix_error",
            "source_jw_mapping_error_vs_eta.png",
        ),
    ]
    for xlabel, ylabel, key, filename in plots:
        plt.figure(figsize=(7.0, 4.6))
        for levels in levels_values:
            plt.plot(arr(levels, "eta"), arr(levels, key), marker="o", linewidth=1.8, label=f"N={levels}")
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.grid(True, alpha=0.3)
        plt.legend(title="levels")
        plt.tight_layout()
        plt.savefig(output_dir / filename, dpi=180)
        plt.close()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--levels", default="3,4,5", help="comma-separated level counts")
    parser.add_argument("--g", type=float, default=0.7)
    parser.add_argument("--eta-min", type=float, default=1e-4)
    parser.add_argument("--eta-max", type=float, default=0.2)
    parser.add_argument("--points", type=int, default=12)
    parser.add_argument("--output-dir", default="source-results")
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    levels_values = [int(item.strip()) for item in args.levels.split(",") if item.strip()]
    eta_values = np.geomspace(args.eta_min, args.eta_max, args.points)
    rows = run_source_sweep(levels_values, eta_values, args.g)

    save_csv(rows, output_dir / "source_sweep_results.csv")
    plot_source_sweeps(rows, output_dir)

    print(f"Wrote {len(rows)} rows to {output_dir / 'source_sweep_results.csv'}")
    print(f"Wrote source figures to {output_dir}")


if __name__ == "__main__":
    main()
