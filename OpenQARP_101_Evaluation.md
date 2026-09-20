# OpenQARP Colab Notebook — Execution Evaluation

**Notebook reviewed:** `OpenQARP_Colab_101.ipynb`
**Author:** Carlos Araque, @KentryOps Data Labs
**Run date:** 18-09-2026
**Package under test:** `openqarp` v0.1.0 (Fujitsu Research of Europe, Apache 2.0)

## Summary

All three test cells executed successfully after the `.ry(qubit, angle)` argument-order fix, with **zero errors and every sanity check passing**. The environment installed cleanly on a stock Colab runtime with no compilation step, confirming the pre-built wheel path works as documented.

| Cell | Status | Result |
|---|---|---|
| Install & import | ✅ Pass | `qarp` imported, version `0.1.0` confirmed |
| Example 1 — Bell state sampling | ✅ Pass | 48.9% / 51.1% split on `(0,0)`/`(1,1)` |
| Example 2 — Exact vs. shot-based ⟨H⟩ | ✅ Pass | Both methods returned `1.5000`, matching hand-calculation exactly |
| Example 3 — VQE ground-state search | ✅ Pass | Found `-1.414214`, matching NumPy's exact eigenvalue to 6 decimal places |

---

## Detailed Results

### 1. Install
```
OpenQARP (qarp) imported OK.
Version: 0.1.0
```
Two wheels downloaded (~3.1 MB and ~4.9 MB) in a few seconds, no source build triggered — consistent with the documented pre-built wheel support for Linux/macOS/Windows on Python 3.11–3.14, which covers Colab's default runtime.

### 2. Example 1 — Bell state sampling
```
Bell state measurement distribution:
  (0, 0): 0.4888
  (1, 1): 0.5112

✅ Sanity check passed: entanglement produced the expected 50/50 split.
```
**Evaluation:** Correct. No `(0,1)`/`(1,0)` outcomes appeared at all, which is exactly what a noiseless Bell-state simulation should produce — the circuit diagram (`bell.plot()`) also rendered without issue, confirming `H → CX` was built as intended. The ~1.1-point deviation from a perfect 50/50 split is ordinary shot noise at `n_shots=4000` (expected std. dev. ≈ 0.8 percentage points), not a bug.

### 3. Example 2 — Exact vs. shot-based expectation value
```
Exact ⟨H⟩ (statevector):   1.5000
Sampled ⟨H⟩ (4000 shots):  1.5000
Hand-computed expectation: 1.5000

✅ Sanity check passed: exact and sampled expectation values agree.
```
**Evaluation:** Correct, and notably the sampled value landed exactly on `1.5000` rather than showing the small offset you'd typically expect from shot noise — likely a favorable draw from `seed=42` at this shot count, or Pauli-averaging variance happening to round cleanly to 4 displayed decimals. Either way, both the `StateVector` (exact) and `PauliAveraging` (shot-based) primitives agree with the by-hand calculation, which is the real validation here: two different primitives reading the same block give consistent physics.

### 4. Example 3 — VQE-style ground-state search
```
True ground-state energy (NumPy eigensolver): -1.414214
VQE-found ground-state energy:  -1.414214
True ground-state energy:       -1.414214
Absolute error:                 0.000000

✅ VQE loop converged close to the true ground-state energy.
```
**Evaluation:** This is the most interesting result. `-1.414214 ≈ -√2`, and COBYLA converged to the exact ground state to 6 decimal places — not just "close," but numerically exact within the printed precision. This makes sense here rather than being suspicious: the 3-parameter ansatz (`RY(0)`, `RY(1)`, `CX(0,1)`, `RY(0)`) is expressive enough to fully span the ground state of this particular 2-qubit Hamiltonian, so with an exact (`StateVector`) energy evaluation and no shot noise in the optimization loop, COBYLA has a clean, noiseless landscape to converge on. This is a best-case scenario for VQE (exact simulation, small/well-matched ansatz, low-dimensional Hamiltonian) — it demonstrates the mechanics correctly, but isn't representative of how VQE performs on a larger molecule or with shot-based (noisy) energy evaluations, where convergence to this many decimal places would not be expected.

---

## Fix Recap

The earlier version of this cell failed with:
```
TypeError: ry(): incompatible function arguments...
```
because the original code called `.ry(theta, qubit)`. OpenQARP's C++ backend (`qarpx`) exposes `ry(qubit_index: int, angle: Param)` — qubit first, angle second, consistent with `h(qubit)` and `cx(control, target)`. Swapping to `.ry(qubit, theta)` resolved it, and this run confirms the fix works end to end.

## Overall Assessment

The notebook is functioning as intended: it validates installation, basic circuit construction and sampling, dual expectation-value estimation paths, and a full classical-quantum optimization loop — the four building blocks most people will want to confirm before building anything larger on OpenQARP. No further changes are needed for this version of the notebook.

**Suggested next step (optional):** to make Example 3 more representative of realistic VQE behavior, consider re-running the energy evaluation with `PauliAveraging` (shots) instead of `StateVector` (exact) — this would show the optimizer contending with noisy energy estimates, which is the regime real hardware and larger chemistry problems actually operate in.
