# Pair-Source Extension

## Motivation

In an exactly diagonalized finite BCS Hamiltonian with particle-number
conservation, the anomalous amplitude

```text
<P_j> = <c_{j down} c_{j up}>
```

vanishes by symmetry. This makes a direct comparison with the broken-symmetry
BCS anomalous profile impossible unless a source field is introduced.

## Implemented Source Term

The finite model now supports

```text
H_eta = H - eta sum_j (P_j^dagger + P_j).
```

The source `eta` explicitly breaks particle-number symmetry. The physically
interesting procedure is to study finite systems at small nonzero `eta`, then
analyze the trend toward `eta -> 0` and increasing system size.

## New Diagnostics

The benchmark now reports:

- `source_pair_norm`: norm of the exact anomalous vector `<P_j>_eta`;
- `bcs_pair_norm`: norm of the projected BCS anomalous profile;
- `relative_source_profile_error`: relative profile error after phase alignment;
- `jw_mapping_matrix_error`: matrix-level check that the Pauli-string Hamiltonian still matches the fermionic Hamiltonian.

## Scientific Interpretation

The pair-density residual remains the correct number-conserving diagnostic.
The source-field diagnostic adds a complementary test:

```text
Does the exact finite system, when gently symmetry-broken, align with the BCS anomalous pair profile?
```

This directly addresses the most delicate physics in the project: the relation
between finite exact diagonalization, explicit symmetry breaking, and the BCS
mean-field limit.
