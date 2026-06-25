# Hierarchical BCS Manuscript

This repository contains a hierarchical equation-of-motion study of the reduced
BCS Hamiltonian, with finite-size quantum-simulation benchmarks.

`C:\Users\aocbaeta\Downloads\CONTINUACAO_CODEX_HIERARCHICAL_BCS.md`

## PDF Status

The actively maintained final PDF is:

- `relatorio_final_tecnico.pdf`

This file is regenerated whenever the analysis, reports, figures, or numerical
results are updated.

The files below are retained as archival manuscript snapshots:

- `main.pdf`
- `main_expanded.pdf`

They are not the current final report. The LaTeX source files were intentionally
removed from the GitHub repository, so the active deliverable is the compiled
technical report PDF plus the Markdown reports and reproducible Python scripts.

Files:

- `references.bib`: bibliography for the core comparison literature.
- `NOVELTY_AUDIT.md`: conservative separation between established literature, demonstrated claims, and open formalization.
- `RELATORIO_FINAL.md`: Portuguese scientific summary in Markdown.
- `SOURCE_FIELD_REPORT.md`: source-field extension report.
- `relatorio_final_tecnico.pdf`: current compiled PDF of the final technical report.
- `main.pdf`, `main_expanded.pdf`: archival manuscript PDFs.
- `quantum-bcs-lab/`: finite BCS computational companion using exact diagonalization plus Qiskit, PennyLane, and Cirq layers.

Computational benchmark:

```powershell
cd quantum-bcs-lab
python run_benchmark.py --levels 4 --g 0.7
python run_benchmark.py --levels 4 --g 0.7 --eta 0.01
python run_sweeps.py --levels 3,4,5 --g-min 0.1 --g-max 1.4 --points 14 --output-dir results
python run_source_sweeps.py --levels 3,4,5 --g 0.7 --eta-min 1e-4 --eta-max 0.2 --points 12 --output-dir source-results
python run_scaling_sweeps.py --levels 3,4,5,6,7,8,9,10 --g 0.7 --eta-min 1e-4 --eta-max 0.2 --points 10 --output-dir scaling-results
python run_large_scaling_sweeps.py --levels 6,8,10,12,14,16 --etas 0.02,0.05,0.1,0.2 --g 0.7 --output-dir large-scaling-results
python run_extrapolation.py --input scaling-results/scaling_sweep_results.csv --output-dir extrapolation-results
python run_phase_sweeps.py --levels 8 --g 0.7 --eta 0.05 --points 16 --output-dir phase-results
python test_consistency.py
```

Scientific caution:

- The second-order pair-sector closure is presented as the demonstrated core of the draft.
- Higher recursive closure maps, Banach-space convergence, homological algebra, and hierarchical information measures are presented as proposed formalization, not established results.
