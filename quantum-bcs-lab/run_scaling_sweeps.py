"""Scaling sweeps in the pair subspace for the eta -> 0 question."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from bcs_core import default_model, exact_ground_state, source_response
from pairspace_core import (
    exact_pairspace_ground_state,
    pairspace_density_residual,
    pairspace_source_response,
)


def validate_pairspace(levels: int, g: float, eta: float) -> dict:
    model = default_model(n_levels=levels, g=g, eta=eta)
    full = exact_ground_state(model)
    pair = exact_pairspace_ground_state(model)
    full_source = source_response(model, full["state"])
    pair_source = pairspace_source_response(model, pair["state"])
    return {
        "energy_difference": abs(full["energy"] - pair["energy"]),
        "source_norm_difference": abs(full_source["source_pair_norm"] - pair_source["source_pair_norm"]),
    }


def run_scaling(levels_values: list[int], eta_values: np.ndarray, g: float) -> list[dict]:
    rows: list[dict] = []
    for levels in levels_values:
        for eta in eta_values:
            model = default_model(n_levels=levels, g=g, eta=float(eta))
            exact = exact_pairspace_ground_state(model)
            source = pairspace_source_response(model, exact["state"])
            density = pairspace_density_residual(model, exact["state"])
            rows.append(
                {
                    "levels": levels,
                    "pairspace_dim": 2**levels,
                    "g": g,
                    "eta": float(eta),
                    "exact_pairspace_energy": exact["energy"],
                    "source_pair_norm": source["source_pair_norm"],
                    "bcs_pair_norm": source["bcs_pair_norm"],
                    "relative_source_profile_error": source["relative_source_profile_error"],
                    "leading_pair_density_eigenvalue": density["leading_pair_density_eigenvalue"],
                    "relative_pair_density_residual": density["relative_pair_density_residual"],
                }
            )
    return rows


def save_csv(rows: list[dict], path: Path) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def plot_scaling(rows: list[dict], output_dir: Path) -> None:
    levels_values = sorted({row["levels"] for row in rows})
    eta_values = sorted({row["eta"] for row in rows})

    def by_level(levels: int, key: str) -> tuple[np.ndarray, np.ndarray]:
        subset = sorted([row for row in rows if row["levels"] == levels], key=lambda item: item["eta"])
        return np.array([row["eta"] for row in subset]), np.array([row[key] for row in subset])

    for ylabel, key, filename in [
        ("||<P>_eta||", "source_pair_norm", "scaling_source_norm_vs_eta.png"),
        ("Relative source-profile error", "relative_source_profile_error", "scaling_source_error_vs_eta.png"),
        ("Relative pair-density residual", "relative_pair_density_residual", "scaling_pair_residual_vs_eta.png"),
    ]:
        plt.figure(figsize=(7.2, 4.7))
        for levels in levels_values:
            x, y = by_level(levels, key)
            plt.semilogx(x, y, marker="o", linewidth=1.7, label=f"N={levels}")
        plt.xlabel("pair source eta")
        plt.ylabel(ylabel)
        plt.grid(True, alpha=0.3)
        plt.legend(title="levels")
        plt.tight_layout()
        plt.savefig(output_dir / filename, dpi=180)
        plt.close()

    fixed_etas = [eta_values[0], eta_values[len(eta_values) // 2], eta_values[-1]]
    for ylabel, key, filename in [
        ("||<P>_eta||", "source_pair_norm", "scaling_source_norm_vs_n.png"),
        ("Relative source-profile error", "relative_source_profile_error", "scaling_source_error_vs_n.png"),
    ]:
        plt.figure(figsize=(7.2, 4.7))
        for eta in fixed_etas:
            subset = sorted([row for row in rows if row["eta"] == eta], key=lambda item: item["levels"])
            plt.plot(
                [row["levels"] for row in subset],
                [row[key] for row in subset],
                marker="o",
                linewidth=1.7,
                label=f"eta={eta:.2g}",
            )
        plt.xlabel("number of pair levels N")
        plt.ylabel(ylabel)
        plt.grid(True, alpha=0.3)
        plt.legend()
        plt.tight_layout()
        plt.savefig(output_dir / filename, dpi=180)
        plt.close()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--levels", default="3,4,5,6,7,8,9,10")
    parser.add_argument("--g", type=float, default=0.7)
    parser.add_argument("--eta-min", type=float, default=1e-4)
    parser.add_argument("--eta-max", type=float, default=0.2)
    parser.add_argument("--points", type=int, default=10)
    parser.add_argument("--output-dir", default="scaling-results")
    parser.add_argument("--validate-levels", type=int, default=4)
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    levels_values = [int(item.strip()) for item in args.levels.split(",") if item.strip()]
    eta_values = np.geomspace(args.eta_min, args.eta_max, args.points)
    rows = run_scaling(levels_values, eta_values, args.g)
    save_csv(rows, output_dir / "scaling_sweep_results.csv")
    plot_scaling(rows, output_dir)

    validation = validate_pairspace(args.validate_levels, args.g, float(eta_values[min(2, len(eta_values) - 1)]))
    with (output_dir / "pairspace_validation.txt").open("w", encoding="utf-8") as handle:
        for key, value in validation.items():
            handle.write(f"{key}: {value:.16e}\n")

    print(f"Wrote {len(rows)} rows to {output_dir / 'scaling_sweep_results.csv'}")
    print(f"Wrote scaling figures to {output_dir}")
    print("Pairspace validation:", validation)


if __name__ == "__main__":
    main()
