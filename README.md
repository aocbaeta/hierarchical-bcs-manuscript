# Hierarchical BCS Manuscript

This folder contains a first LaTeX manuscript draft based on the continuation notes in:

`C:\Users\aocbaeta\Downloads\CONTINUACAO_CODEX_HIERARCHICAL_BCS.md`

Files:

- `main.tex`: article draft in REVTeX/Physical Review style.
- `references.bib`: bibliography for the core comparison literature.
- `NOVELTY_AUDIT.md`: conservative separation between established literature, demonstrated claims, and open formalization.
- `RELATORIO_FINAL.md`: Portuguese scientific summary in Markdown.
- `relatorio_final_tecnico.tex`: final technical report with sweep figures.
- `relatorio_final_tecnico.pdf`: compiled PDF of the final technical report.
- `main_expanded.pdf`: compiled manuscript copy with expanded appendices.
- `quantum-bcs-lab/`: finite BCS computational companion using exact diagonalization plus Qiskit, PennyLane, and Cirq layers.

Build command:

```powershell
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

Computational benchmark:

```powershell
cd quantum-bcs-lab
python run_benchmark.py --levels 4 --g 0.7
python run_sweeps.py --levels 3,4,5 --g-min 0.1 --g-max 1.4 --points 14 --output-dir results
```

Scientific caution:

- The second-order pair-sector closure is presented as the demonstrated core of the draft.
- Higher recursive closure maps, Banach-space convergence, homological algebra, and hierarchical information measures are presented as proposed formalization, not established results.
