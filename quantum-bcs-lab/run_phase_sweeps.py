"""Complex source phase sweep for the pair-subspace BCS model."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from bcs_core import default_model
from pairspace_core import exact_pairspace_ground_state, pairspace_source_response


def phase_difference(a: float, b: float) -> float:
    return float(np.angle(np.exp(1j * (a - b))))


def run_phase_sweep(levels: int, g: float, eta_abs: float, points: int) -> list[dict]:
    rows = []
    for phase in np.linspace(0.0, 2.0 * np.pi, points, endpoint=False):
        model = default_model(n_levels=levels, g=g, eta=eta_abs * np.exp(1j * phase))
        exact = exact_pairspace_ground_state(model)
        source = pairspace_source_response(model, exact["state"])
        rows.append(
            {
                "levels": levels,
                "g": g,
                "eta_abs": eta_abs,
                "eta_phase": phase,
                "source_pair_phase": source["source_pair_phase"],
                "phase_difference": phase_difference(source["source_pair_phase"], phase),
                "source_pair_norm": source["source_pair_norm"],
                "relative_source_profile_error": source["relative_source_profile_error"],
            }
        )
    return rows


def save_and_plot(rows: list[dict], output_dir: Path) -> None:
    with (output_dir / "phase_sweep_results.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    eta_phase = np.array([row["eta_phase"] for row in rows])
    source_phase = np.unwrap(np.array([row["source_pair_phase"] for row in rows]))
    ideal = np.unwrap(eta_phase)

    plt.figure(figsize=(7.2, 4.7))
    plt.plot(eta_phase, source_phase, "o-", label="arg sum_j <P_j>")
    plt.plot(eta_phase, ideal, "--", label="arg eta")
    plt.xlabel("source phase arg eta")
    plt.ylabel("response phase")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_dir / "response_phase_vs_eta_phase.png", dpi=180)
    plt.close()

    plt.figure(figsize=(7.2, 4.7))
    plt.plot(eta_phase, [row["phase_difference"] for row in rows], "o-")
    plt.xlabel("source phase arg eta")
    plt.ylabel("phase difference")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_dir / "phase_difference_vs_eta_phase.png", dpi=180)
    plt.close()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--levels", type=int, default=8)
    parser.add_argument("--g", type=float, default=0.7)
    parser.add_argument("--eta", type=float, default=0.05)
    parser.add_argument("--points", type=int, default=16)
    parser.add_argument("--output-dir", default="phase-results")
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    rows = run_phase_sweep(args.levels, args.g, args.eta, args.points)
    save_and_plot(rows, output_dir)
    max_phase_error = max(abs(row["phase_difference"]) for row in rows)
    print(f"Wrote {len(rows)} phase rows to {output_dir}")
    print(f"Max phase difference: {max_phase_error:.6e}")


if __name__ == "__main__":
    main()
