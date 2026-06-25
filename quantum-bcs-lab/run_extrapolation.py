"""Finite-size extrapolation of pair-source scaling data."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit


def read_rows(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8") as handle:
        return [{key: float(value) for key, value in row.items()} for row in csv.DictReader(handle)]


def r2_score(y: np.ndarray, pred: np.ndarray) -> float:
    ss_res = float(np.sum((y - pred) ** 2))
    ss_tot = float(np.sum((y - np.mean(y)) ** 2))
    return 1.0 - ss_res / ss_tot if ss_tot > 0 else 1.0


def corrected_aic(y: np.ndarray, pred: np.ndarray, k: int) -> float:
    n = len(y)
    rss = max(float(np.sum((y - pred) ** 2)), 1e-300)
    aic = n * np.log(rss / n) + 2 * k
    if n - k - 1 <= 0:
        return aic
    return aic + (2 * k * (k + 1)) / (n - k - 1)


def power_offset(n: np.ndarray, asymptote: float, amplitude: float, exponent: float) -> np.ndarray:
    return asymptote + amplitude * n ** (-exponent)


def fit_models_for_eta(n: np.ndarray, y: np.ndarray) -> list[dict]:
    x = 1.0 / n
    fits: list[dict] = []

    linear = np.polyfit(x, y, deg=1)
    pred_linear = linear[0] * x + linear[1]
    fits.append(
        {
            "model": "linear_1_over_n",
            "error_infinite_n": float(linear[1]),
            "param_1": float(linear[0]),
            "param_2": 0.0,
            "r2": r2_score(y, pred_linear),
            "aicc": corrected_aic(y, pred_linear, 2),
            "rmse": float(np.sqrt(np.mean((y - pred_linear) ** 2))),
        }
    )

    quadratic = np.polyfit(x, y, deg=2)
    pred_quadratic = quadratic[0] * x**2 + quadratic[1] * x + quadratic[2]
    fits.append(
        {
            "model": "quadratic_1_over_n",
            "error_infinite_n": float(quadratic[2]),
            "param_1": float(quadratic[1]),
            "param_2": float(quadratic[0]),
            "r2": r2_score(y, pred_quadratic),
            "aicc": corrected_aic(y, pred_quadratic, 3),
            "rmse": float(np.sqrt(np.mean((y - pred_quadratic) ** 2))),
        }
    )

    try:
        popt, _ = curve_fit(
            power_offset,
            n,
            y,
            p0=[max(0.0, y[-1] * 0.5), max(1e-6, y[0] - y[-1]), 1.0],
            bounds=([0.0, -10.0, 0.05], [2.0, 10.0, 5.0]),
            maxfev=20000,
        )
        pred_power = power_offset(n, *popt)
        fits.append(
            {
                "model": "power_offset",
                "error_infinite_n": float(popt[0]),
                "param_1": float(popt[1]),
                "param_2": float(popt[2]),
                "r2": r2_score(y, pred_power),
                "aicc": corrected_aic(y, pred_power, 3),
                "rmse": float(np.sqrt(np.mean((y - pred_power) ** 2))),
            }
        )
    except (RuntimeError, ValueError):
        pass

    return fits


def fit_vs_inverse_n(rows: list[dict], output_dir: Path) -> list[dict]:
    etas = sorted({row["eta"] for row in rows})
    fits = []
    for eta in etas:
        subset = sorted([row for row in rows if row["eta"] == eta], key=lambda row: row["levels"])
        n = np.array([row["levels"] for row in subset], dtype=float)
        y = np.array([row["relative_source_profile_error"] for row in subset], dtype=float)
        for fit in fit_models_for_eta(n, y):
            fit["eta"] = eta
            fits.append(fit)

    best_fits = []
    for eta in etas:
        eta_fits = [fit for fit in fits if fit["eta"] == eta]
        best = min(eta_fits, key=lambda fit: fit["aicc"]).copy()
        best_fits.append(best)

    with (output_dir / "extrapolation_fits.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["eta", "model", "error_infinite_n", "param_1", "param_2", "r2", "aicc", "rmse"])
        writer.writeheader()
        writer.writerows(fits)

    with (output_dir / "extrapolation_best_fits.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["eta", "model", "error_infinite_n", "param_1", "param_2", "r2", "aicc", "rmse"])
        writer.writeheader()
        writer.writerows(best_fits)

    eta_arr = np.array([row["eta"] for row in best_fits])
    inf_err = np.array([row["error_infinite_n"] for row in best_fits])
    plt.figure(figsize=(7.2, 4.7))
    plt.semilogx(eta_arr, inf_err, marker="o", linewidth=1.8)
    plt.xlabel("pair source eta")
    plt.ylabel("best-model extrapolated error at N -> infinity")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_dir / "extrapolated_error_vs_eta.png", dpi=180)
    plt.close()

    selected = [etas[0], etas[len(etas) // 2], etas[-1]]
    plt.figure(figsize=(7.2, 4.7))
    for eta in selected:
        subset = sorted([row for row in rows if row["eta"] == eta], key=lambda row: row["levels"])
        n = np.array([row["levels"] for row in subset], dtype=float)
        x = 1.0 / n
        y = np.array([row["relative_source_profile_error"] for row in subset], dtype=float)
        coeff = np.polyfit(x, y, deg=1)
        grid = np.linspace(0.0, max(x), 100)
        plt.plot(x, y, "o", label=f"data eta={eta:.2g}")
        plt.plot(grid, coeff[0] * grid + coeff[1], "-", alpha=0.8)
    plt.xlabel("1/N")
    plt.ylabel("relative source-profile error")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_dir / "error_vs_inverse_n_fits.png", dpi=180)
    plt.close()

    plt.figure(figsize=(7.2, 4.7))
    for model in sorted({fit["model"] for fit in fits}):
        subset = sorted([fit for fit in fits if fit["model"] == model], key=lambda fit: fit["eta"])
        plt.semilogx(
            [fit["eta"] for fit in subset],
            [fit["error_infinite_n"] for fit in subset],
            marker="o",
            linewidth=1.5,
            label=model,
        )
    plt.xlabel("pair source eta")
    plt.ylabel("extrapolated error at N -> infinity")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_dir / "model_comparison_extrapolated_error.png", dpi=180)
    plt.close()

    return best_fits


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="scaling-results/scaling_sweep_results.csv")
    parser.add_argument("--output-dir", default="extrapolation-results")
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    fits = fit_vs_inverse_n(read_rows(Path(args.input)), output_dir)
    print(f"Wrote {len(fits)} extrapolation rows to {output_dir}")


if __name__ == "__main__":
    main()
