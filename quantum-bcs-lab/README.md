# Quantum BCS Lab

Computational companion to the hierarchical BCS manuscript.

The goal is to compare four views of the same finite reduced-BCS model:

1. exact diagonalization;
2. projected BCS gap closure;
3. qubit Hamiltonian under Jordan-Wigner mapping;
4. Qiskit, PennyLane, and Cirq implementations.

## Model

For `n_levels` pair levels, the qubit convention is:

- qubit `2*j`: mode `k_j up`;
- qubit `2*j + 1`: mode `-k_j down`.

The Hamiltonian is

```text
H = sum_j xi_j (n_{j up} + n_{j down})
    - g sum_{j,l} P_j^\dagger P_l
    - eta sum_j (P_j^\dagger + P_j)
```

where `P_j = c_{j down} c_{j up}`.

The `eta` term is optional. It explicitly breaks particle-number symmetry and
lets exact diagonalization produce nonzero anomalous pair amplitudes `<P_j>`.

## Run Now

The core benchmark only needs `numpy` and runs on the current machine:

```powershell
python run_benchmark.py --levels 4 --g 0.7
python run_benchmark.py --levels 4 --g 0.7 --eta 0.01
python run_source_sweeps.py --levels 3,4,5 --g 0.7 --eta-min 1e-4 --eta-max 0.2 --points 12 --output-dir source-results
python run_scaling_sweeps.py --levels 3,4,5,6,7,8,9,10 --g 0.7 --eta-min 1e-4 --eta-max 0.2 --points 10 --output-dir scaling-results
python run_extrapolation.py --input scaling-results/scaling_sweep_results.csv --output-dir extrapolation-results
python run_phase_sweeps.py --levels 8 --g 0.7 --eta 0.05 --points 16 --output-dir phase-results
python test_consistency.py
```

It reports:

- exact ground-state energy;
- BCS mean-field/projected-closure energy;
- gap from the projected closure;
- leading eigenvalue of the exact pair-density matrix;
- residual pair-density error;
- pair-source amplitude norm when `eta != 0`;
- source-profile error relative to the projected BCS anomalous profile;
- Jordan-Wigner mapping consistency error.

## Optional Quantum Frameworks

Install the full stack:

```powershell
pip install -r requirements.txt
```

Then run:

```powershell
python qiskit_bcs_exact.py
python pennylane_bcs_vqe.py
python cirq_bcs_dynamics.py
```

## Connection to the Manuscript

The quantity `relative_pair_density_residual` is a first numerical diagnostic for the hierarchy idea:

```text
exact pair-density matrix  vs.  rank-one pair-sector projected density
```

Small residual means the lowest pair-sector closure captures the exact finite model well. Large residual means omitted hierarchy sectors are important and should be represented by higher closure maps.

With `eta != 0`, the additional quantity `relative_source_profile_error` compares:

```text
exact source-induced anomalous profile <P_j>_eta  vs.  BCS anomalous profile
```

This is the direct finite-system probe of the symmetry-breaking limit.

## Pair-Subspace Scaling

The reduced BCS model with the pair source remains inside the pair subspace,
where each level is either empty or occupied by a complete pair. The file
`pairspace_core.py` uses this representation, reducing the Hilbert-space
dimension from `2**(2*N)` to `2**N`.

`run_scaling_sweeps.py` uses the pair-subspace Hamiltonian to reach `N=10`.
It also validates the pair-subspace result against the full fermionic
Hamiltonian for a small system.

## Extrapolation and Phase

`run_extrapolation.py` compares linear `1/N`, quadratic `1/N`, and offset
power-law finite-size models at fixed `eta`, then selects the best model by
AICc to estimate the `N -> infinity` trend.

`run_phase_sweeps.py` uses a complex source

```text
H_eta = H - sum_j (eta P_j^dagger + eta* P_j)
```

and verifies that the anomalous response phase follows `arg(eta)`.
