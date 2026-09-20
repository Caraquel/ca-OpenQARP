# ca-OpenQARP

OpenQARP learning notebooks by Carlos Araque / Caraquel.

This project starts with a working installation and examples notebook, then
develops a more detailed tutorial and training path.

## Tutorial index

| Notebook | Purpose | Status |
| --- | --- | --- |
| [101 — Quick start](OpenQARP_Colab_101.ipynb) | Install OpenQARP; sample a Bell state; compare expectation values; run a small VQE-style search. | Working baseline reported by the author; preserved unchanged. |
| [102 — Guided tutorial](OpenQARP_Colab_102_Tutorial.ipynb) | Follow the baseline code with learning objectives, mathematical explanations, exercises, and a results log. | Initial training edition; fresh Colab execution pending. |

## Run a notebook

1. Open Google Colab and choose **File → Upload notebook**, then select 101 or 102.
2. Connect to a Python runtime and run cells from top to bottom, starting with installation.
3. Check the printed results and assertions. The final optimization example reports
   whether its energy is close to the reference; a convergence warning is a result
   to investigate, not proof of a broken installation.
4. Use 102 for changes and exercises. Keep 101 as the original reference.

The installation cell currently installs the available `openqarp` release without
a version pin. Record the installed version and runtime when comparing runs;
future dependency releases may change behavior.

## Project progress

- [x] Keep the original 101 notebook as the baseline.
- [x] Create 102 with the same executable examples and added training material.
- [x] Exclude `Ignore_folder/` and Jupyter checkpoints from Git.
- [ ] Run 102 in a fresh Colab runtime and record package versions and results.
- [ ] Complete the Bell-state and expectation-value exercises.
- [ ] Compare optimization seeds, iteration budgets, and energy errors.
- [ ] Add further tutorials after validating their examples.

### Progress log

| Date | Update | Validation |
| --- | --- | --- |
| 2026-09-20 | Preserved 101; added guided 102 notebook, ignore rules, and tutorial tracking. | Notebook structure and code-copy checks performed locally; fresh Colab run pending. |

When adding a tutorial, add it to the index, describe its prerequisites and expected
results, and update this log with the runtime, package version, and execution outcome.

## Local experiments

`Ignore_folder/` holds private scratch files and experiments. Its contents stay on
disk but are excluded from future Git tracking. Ignore rules do not remove files
from existing Git history. Promote useful experiments into a named tutorial at the
repository root when they are ready to review.

## Upstream resources

These are the upstream links included in the baseline notebook:

- [OpenQARP repository and examples](https://github.com/OpenQARP/openqarp)
- [OpenQARP documentation](https://openqarp.github.io/openqarp/)

This README tracks this project's learning material; it is not the upstream
OpenQARP documentation.
