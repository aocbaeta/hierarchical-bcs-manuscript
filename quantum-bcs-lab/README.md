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
```

where `P_j = c_{j down} c_{j up}`.

## Run Now

The core benchmark only needs `numpy` and runs on the current machine:

```powershell
python run_benchmark.py --levels 4 --g 0.7
```

It reports:

- exact ground-state energy;
- BCS mean-field/projected-closure energy;
- gap from the projected closure;
- leading eigenvalue of the exact pair-density matrix;
- residual pair-density error;
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
