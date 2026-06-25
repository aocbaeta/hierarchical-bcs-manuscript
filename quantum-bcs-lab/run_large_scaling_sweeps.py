"""Large-N pair-subspace scaling sweeps using sparse diagonalization."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from bcs_core import default_model
from pairspace_core import exact_pairspace_ground_state_sparse, pairspace_source_response


def run_large_scaling(levels_values: list[int], eta_values: list[float], g: float) -> list[dict]:
    rows = []
    for levels in levels_values:
        for eta in eta_values:
            model = default_model(n_levels=levels, g=g, eta=eta)
            exact = exact_pairspace_ground_state_sparse(model)
            source = pairspace_source_response(model, exact["state"])
            rows.append(
                {
                    "levels": levels,
                    "pairspace_dim": 2**levels,
                    "hamiltonian_nnz": exact["hamiltonian_nnz"],
                    "g": g,
                    "eta": eta,
                    "exact_pairspace_energy": exact["energy"],
                    "source_pair_norm": source["source_pair_norm"],
                    "bcs_pair_norm": source["bcs_pair_norm"],
                    "relative_source_profile_error": source["relative_source_profile_error"],
                }
            )
            print(
                f"N={levels:2d} eta={eta:.4g} "
                f"norm={source['source_pair_norm']:.6g} "
                f"err={source['relative_source_profile_error']:.6g}"
            )
    return rows


def save_csv(rows: list[dict], path: Path) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def plot_large_scaling(rows: list[dict], output_dir: Path) -> None:
    etas = sorted({row["eta"] for row in rows})

    for ylabel, key, filename in [
        ("||<P>_eta||", "source_pair_norm", "large_source_norm_vs_n.png"),
        ("Relative source-profile error", "relative_source_profile_error", "large_source_error_vs_n.png"),
    ]:
        plt.figure(figsize=(7.2, 4.7))
        for eta in etas:
            subset = sorted([row for row in rows if row["eta"] == eta], key=lambda row: row["levels"])
            plt.plot(
                [row["levels"] for row in subset],
                [row[key] for row in subset],
                marker="o",
                linewidth=1.8,
                label=f"eta={eta:g}",
            )
        plt.xlabel("number of pair levels N")
        plt.ylabel(ylabel)
        plt.grid(True, alpha=0.3)
        plt.legend()
        plt.tight_layout()
        plt.savefig(output_dir / filename, dpi=180)
        plt.close()


def fit_large_scaling(rows: list[dict], output_dir: Path) -> list[dict]:
    fits = []
    for eta in sorted({row["eta"] for row in rows}):
        subset = sorted([row for row in rows if row["eta"] == eta], key=lambda row: row["levels"])
        n = np.array([row["levels"] for row in subset], dtype=float)
        y = np.array([row["relative_source_profile_error"] for row in subset], dtype=float)
        x = 1.0 / n
        coeff = np.polyfit(x, y, deg=1)
        pred = coeff[0] * x + coeff[1]
        rmse = float(np.sqrt(np.mean((y - pred) ** 2)))
        fits.append(
            {
                "eta": eta,
                "error_infinite_n_linear": float(coeff[1]),
                "slope_1_over_n": float(coeff[0]),
                "rmse": rmse,
            }
        )

    with (output_dir / "large_scaling_fits.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fits[0].keys()))
        writer.writeheader()
        writer.writerows(fits)

    plt.figure(figsize=(7.2, 4.7))
    plt.semilogx(
        [row["eta"] for row in fits],
        [row["error_infinite_n_linear"] for row in fits],
        marker="o",
        linewidth=1.8,
    )
    plt.xlabel("pair source eta")
    plt.ylabel("large-N linear extrapolated error")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_dir / "large_extrapolated_error_vs_eta.png", dpi=180)
    plt.close()
    return fits


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--levels", default="6,8,10,12,14,16")
    parser.add_argument("--etas", default="0.02,0.05,0.1,0.2")
    parser.add_argument("--g", type=float, default=0.7)
    parser.add_argument("--output-dir", default="large-scaling-results")
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    levels_values = [int(item.strip()) for item in args.levels.split(",") if item.strip()]
    eta_values = [float(item.strip()) for item in args.etas.split(",") if item.strip()]
    rows = run_large_scaling(levels_values, eta_values, args.g)
    save_csv(rows, output_dir / "large_scaling_results.csv")
    plot_large_scaling(rows, output_dir)
    fits = fit_large_scaling(rows, output_dir)
    print(f"Wrote {len(rows)} rows and {len(fits)} fits to {output_dir}")


if __name__ == "__main__":
    main()
