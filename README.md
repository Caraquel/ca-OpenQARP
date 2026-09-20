# ca-OpenQARP

OpenQARP learning notebooks by Carlos Araque / Caraquel.

This project starts with a working installation and examples notebook, then
develops a more detailed tutorial and training path.

**Documentation:** [Official OpenQARP documentation](https://docs.openqarp.com/)

Last reviewed: **2026-09-20**.

## Tutorial index

| Notebook | Purpose | Status |
| --- | --- | --- |
| [101 — Quick start](OpenQARP_Colab_101.ipynb) | Install OpenQARP; sample a Bell state; compare expectation values; run a small VQE-style search. | Working baseline reported by the author; preserved unchanged. |
| [102 — Guided tutorial](OpenQARP_Colab_102_Tutorial.ipynb) | Follow the baseline code with learning objectives, mathematical explanations, exercises, and a results log. | Initial training edition; fresh Colab execution pending. |
| [Tutorial 00 — Hello qarpx](OpenQARP_Tutorial_00_Hello_Qarp_Colab.ipynb) | Colab adaptation of the upstream introduction: build a Bell circuit, choose a primitive, run the engine, and read results. | Saved execution counts on all 7 code cells; no saved errors. Fresh execution not verified in this review. |
| [Tutorial 01 — Blocks](OpenQARP_Tutorial_01_Blocks_Colab.ipynb) | Colab adaptation covering circuit builders, composition, measurements, symbolic parameters, and bit order. | Saved execution counts on all 7 code cells; no saved errors. Fresh execution not verified in this review. |

### Learning path

Start with **101** to check the installation and see complete examples. Use
**102** for guided explanations and exercises. Follow **Tutorial 00 → Tutorial 01**
for the upstream tutorial sequence adapted to Colab. The 101/102 numbers identify
this project's notebooks; 00/01 follow the upstream numbering.

The local 00/01 notebooks identify their sources as upstream examples with added
Colab setup cells. Their content has not been compared line by line with the latest
upstream revision during this review.

## Run a notebook

1. Open Google Colab and choose **File → Upload notebook**, then select a notebook from the index.
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
- [x] Add Tutorial 00 and Tutorial 01 to the tutorial index.
- [x] Add the official documentation domain and topic links.
- [ ] Run 102 in a fresh Colab runtime and record package versions and results.
- [ ] Re-run Tutorials 00 and 01 in fresh Colab runtimes and record versions and results.
- [ ] Complete the Bell-state and expectation-value exercises.
- [ ] Compare optimization seeds, iteration budgets, and energy errors.
- [ ] Add further tutorials after validating their examples.

### Progress log

| Date | Update | Validation |
| --- | --- | --- |
| 2026-09-20 | Preserved 101; added guided 102 notebook, ignore rules, and tutorial tracking. | Notebook structure and code-copy checks performed locally; fresh Colab run pending. |
| 2026-09-20 | Reviewed the four local notebooks; indexed Tutorials 00 and 01; updated documentation links and learning path. | Official documentation homepage reachable; 00/01 have saved execution counts and no saved errors. No notebooks executed or modified in this documentation review. |

When adding a tutorial, add it to the index, describe its prerequisites and expected
results, and update this log with the runtime, package version, and execution outcome.

## Local experiments

`Ignore_folder/` holds private scratch files and experiments. Its contents stay on
disk but are excluded from future Git tracking. Ignore rules do not remove files
from existing Git history. Promote useful experiments into a named tutorial at the
repository root when they are ready to review.

## Documentation

Use the [official OpenQARP documentation](https://docs.openqarp.com/) as the main
reference for installation, concepts, and APIs. Its current navigation includes:

- [Getting started](https://docs.openqarp.com/source/getting_started.html)
- [Installation](https://docs.openqarp.com/source/installation.html)
- [Official tutorial guide](https://docs.openqarp.com/source/tutorial.html)
- [Blocks](https://docs.openqarp.com/source/blocks.html)
- [Algorithms](https://docs.openqarp.com/source/algorithms.html)
- [Engines](https://docs.openqarp.com/source/engines.html)
- [Endianness and bit order](https://docs.openqarp.com/source/endianness.html)
- [API documentation](https://docs.openqarp.com/source/api.html)

### Upstream source

- [OpenQARP repository](https://github.com/OpenQARP/openqarp)
- [Upstream example notebooks](https://github.com/OpenQARP/openqarp/tree/main/examples)

The baseline notebook retains its original documentation links. For ongoing study,
use the documentation domain above. This review updates the local project index
and documentation references; it does not establish a new package release or
validate compatibility with a newer release.

This README tracks this project's learning material; it is not the upstream
OpenQARP documentation.
