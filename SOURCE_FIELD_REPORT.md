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

## Scaling Extension

The source-field analysis was extended with a pair-subspace Hamiltonian. In this
representation each level is either empty or occupied by one complete pair, so
the dimension is `2**N` instead of `2**(2*N)`. This allowed sweeps up to
`N = 10` pair levels.

Validation against the full fermionic Hamiltonian at `N = 4` gave:

```text
energy_difference:      8.881784197001252e-16
source_norm_difference: 1.0798653637955624e-16
```

For `g = 0.7` and `eta` from `1e-4` to `0.2`, the source-induced anomalous norm
increased with system size and the large-source profile error decreased:

```text
N = 3:  ||<P>|| at eta=0.2 = 0.3824, profile error = 0.3453
N = 6:  ||<P>|| at eta=0.2 = 0.8991, profile error = 0.1874
N = 10: ||<P>|| at eta=0.2 = 1.3038, profile error = 0.1464
```

This is the first numerical evidence in the project that increasing the pair
space improves alignment between the explicitly symmetry-broken exact state and
the projected BCS anomalous profile.

## Extrapolation and Complex Source

The finite-size extrapolation was refined by comparing three models at each
fixed value of `eta`:

- linear in `1/N`;
- quadratic in `1/N`;
- offset power law `a + b N^{-alpha}`.

Using AICc as a small-sample model-selection criterion, the linear `1/N` model
was selected for all sampled values of `eta`. Representative extrapolated
errors are:

```text
eta = 1.0e-4:  error(N -> infinity) ~= 0.9926
eta = 8.6e-2:  error(N -> infinity) ~= 0.0953
eta = 2.0e-1:  error(N -> infinity) ~= 0.0616
```

The source was also generalized to complex values:

```text
H_eta = H - sum_j (eta P_j^dagger + eta* P_j).
```

For `N = 8`, `g = 0.7`, `|eta| = 0.05`, and 16 source phases, the maximum phase
difference between `arg(sum_j <P_j>)` and `arg(eta)` was:

```text
2.45e-16
```

Thus the exact symmetry-broken finite system follows the phase of the external
pair source to numerical precision.
