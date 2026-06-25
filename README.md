# Hierarchical BCS Manuscript

This folder contains a first LaTeX manuscript draft based on the continuation notes in:

`C:\Users\aocbaeta\Downloads\CONTINUACAO_CODEX_HIERARCHICAL_BCS.md`

Files:

- `references.bib`: bibliography for the core comparison literature.
- `NOVELTY_AUDIT.md`: conservative separation between established literature, demonstrated claims, and open formalization.
- `RELATORIO_FINAL.md`: Portuguese scientific summary in Markdown.
- `SOURCE_FIELD_REPORT.md`: source-field extension report.
- `relatorio_final_tecnico.pdf`: compiled PDF of the final technical report.
- `main_expanded.pdf`: compiled manuscript copy with expanded appendices.
- `quantum-bcs-lab/`: finite BCS computational companion using exact diagonalization plus Qiskit, PennyLane, and Cirq layers.

The LaTeX source files were intentionally removed from the GitHub repository; the compiled PDFs are retained.

Computational benchmark:

```powershell
cd quantum-bcs-lab
python run_benchmark.py --levels 4 --g 0.7
python run_benchmark.py --levels 4 --g 0.7 --eta 0.01
python run_sweeps.py --levels 3,4,5 --g-min 0.1 --g-max 1.4 --points 14 --output-dir results
python run_source_sweeps.py --levels 3,4,5 --g 0.7 --eta-min 1e-4 --eta-max 0.2 --points 12 --output-dir source-results
```

Scientific caution:

- The second-order pair-sector closure is presented as the demonstrated core of the draft.
- Higher recursive closure maps, Banach-space convergence, homological algebra, and hierarchical information measures are presented as proposed formalization, not established results.
