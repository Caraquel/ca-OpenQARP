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

### Tutorials 00–05 — complete series

These six Colab notebooks build from a first circuit to complete quantum
algorithm workflows. Read them in numerical order; each adds a layer to the
previous tutorial. Basic Python and quantum-computing concepts are assumed.

| Tutorial | Description | What you will learn |
| --- | --- | --- |
| [00 — Hello qarpx](OpenQARP_Tutorial_00_Hello_Qarp_Colab.ipynb) | Build and sample a Bell-state circuit in a minimal end-to-end example. | Connect a block, a sampling primitive, and an engine; interpret bit-tuple probabilities and inspect results. |
| [01 — Blocks](OpenQARP_Tutorial_01_Blocks_Colab.ipynb) | Construct circuits from gate builders and compose reusable subcircuits. | Use the build lifecycle, measurements, symbolic parameters, and parameter binding; understand sorted symbols, radians, and LSB-first bit order. |
| [02 — Primitives](OpenQARP_Tutorial_02_Primitives_Colab.ipynb) | Turn circuits into quantities such as distributions, overlaps, expectation values, and transition amplitudes. | Use the bra/operator/ket interface and choose between exact StateVector calculations and finite-shot estimators. |
| [03 — Engines](OpenQARP_Tutorial_03_Engines_Colab.ipynb) | Compile circuits once and reuse them with different parameter values. | Control random seeds, run parameter sweeps with batch_run, evaluate gradients with run_gradient, and get an introduction to device configuration. |
| [04 — Your own variational loop](OpenQARP_Tutorial_04_Variational_Loop_Colab.ipynb) | Find the ground-state energy of a three-qubit transverse-field Ising model with a manually assembled VQE loop, then the built-in VQE algorithm. | Connect an ansatz, estimator, engine, and optimizer; inspect convergence and use gradients in optimization. |
| [05 — The algorithm toolbox](OpenQARP_Tutorial_05_Algorithm_Tour_Colab.ipynb) | Run QAOA on a six-node MaxCut problem and explore the wider algorithm catalogue. | Follow the construct/build/run/results workflow and locate reference examples for ground states, excited states, phase estimation, optimization, and dynamics. |

### Learning path

Start with **101** to check the installation and see complete examples. Use
**102** for guided explanations and exercises. Continue through
**00 → 01 → 02 → 03 → 04 → 05** to study the full stack:
**first circuit → blocks → primitives → engines → variational loop → algorithm toolbox**.

The 101/102 numbers identify this project's introductory notebooks; 00–05 follow
the upstream tutorial numbering. Descriptions above were checked against the
local notebook contents. The notebooks identify their sources as upstream
examples with added Colab setup cells; their content has not been compared line
by line with the latest upstream revision during this review.

### Saved execution status

| Tutorial | Code cells with saved execution counts | Saved errors |
| --- | --- | --- |
| 00 | 7 / 7 | 0 |
| 01 | 7 / 7 | 0 |
| 02 | 6 / 6 | 0 |
| 03 | 6 / 6 | 0 |
| 04 | 8 / 8 | 0 |
| 05 | 3 / 3 | 0 |

These are saved notebook records, not fresh execution results. Re-run each
notebook in a clean runtime before recording it as currently validated.

## Run a notebook

### Research application — benchmark 06

[Open Research 06 — Multi-provider weighted MaxCut](OpenQARP_Research_06_MultiProvider_MaxCut_Colab.ipynb)
extends tutorials 00–05 into a portfolio case study: partition a synthetic
weighted conflict network, solve it classically, and compare a frozen QAOA
circuit across quantum software stacks.

| Component | What the notebook does |
| --- | --- |
| Classical reference | Exhaustive optimum, seeded local search, and an analytic random-partition baseline. |
| Ideal simulation | Independent NumPy reference; Qiskit Aer, Qrisp-generated circuits on Aer, and Fujitsu OpenQARP. |
| Device models | IBM Manila noise snapshot and IQM Adonis target/noise model, both simulated locally with Aer. |
| Real hardware | Optional IBM Runtime and IQM connection, circuit review, submission, job recovery, and result retrieval. Disabled by default. |
| Research evidence | Repeated seeds, sampling intervals, approximation ratios, optimum-hit probability, distribution distance, circuit resources, timings, raw counts, plots, and a ZIP export. |

**Use in Colab:** upload the notebook, run its pinned installation cell in a
fresh Python 3.11–3.13 CPU runtime, and proceed in order. The local comparison
needs no account. Section 8 has separate IBM and IQM connection cells. IBM accepts
`IBM_TOKEN` / `IBM_CRN`, with `IBM_QUANTUM_TOKEN` / `IBM_QUANTUM_CRN` as a fallback
pair; IQM uses `IQM_API_TOKEN`. IBM lists your devices before you select a backend.
IQM includes a Qrisp connection (Garnet or another entitled device), a separate
benchmark adapter, and an optional `plus.get_measurement()` example. The current
MaxCut hardware profile supports direct-coupling IQM devices; the Sirius Qrisp
example is separate. Previously authenticated objects can also be reused.

Read the [improved research prompt and design brief](Research_Benchmark_Brief.md).
The [dependency profile](requirements-research06.txt) matches the notebook.
See the [local validation report and sample results](reports/research06/VALIDATION.md):
25 simulator runs completed, correctness checks passed, and local dependencies
passed `pip check`. Fresh Colab and real-hardware execution remain pending.
Results are written under ignored `benchmark_results/`; download the generated
ZIP from Colab before disconnecting. Hardware ledgers prevent accidental repeat
submissions and should be retained when restoring a session.

Qrisp is a circuit framework, and IQM's fake backend uses Aer internally.
Different bundled noise models cannot establish a hardware-vendor ranking.
Small simulated examples and API timings do not establish quantum advantage.

### Introductory and tutorial notebooks

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
- [x] Index all six tutorials (00–05) with descriptions, learning outcomes, and local notebook links.
- [x] Add the official documentation domain and topic links.
- [x] Add Research 06 with a classical baseline, simulator benchmark, and optional hardware workflow.
- [ ] Run Research 06 in a fresh Google Colab runtime and record that environment.
- [ ] Evaluate frozen Research 06 circuits on entitled IBM/IQM hardware and retain job evidence.
- [ ] Run 102 in a fresh Colab runtime and record package versions and results.
- [ ] Re-run Tutorials 00–05 in fresh Colab runtimes and record versions and results.
- [ ] Complete the Bell-state and expectation-value exercises.
- [ ] Compare optimization seeds, iteration budgets, and energy errors.
- [ ] Add further tutorials after validating their examples.

### Progress log

| Date | Update | Validation |
| --- | --- | --- |
| 2026-09-20 | Preserved 101; added guided 102 notebook, ignore rules, and tutorial tracking. | Notebook structure and code-copy checks performed locally; fresh Colab run pending. |
| 2026-09-20 | Reviewed the four local notebooks; indexed Tutorials 00 and 01; updated documentation links and learning path. | Official documentation homepage reachable; 00/01 have saved execution counts and no saved errors. No notebooks executed or modified in this documentation review. |
| 2026-09-20 | Expanded the tutorial presentation to the complete 00–05 series, including descriptions, learning outcomes, and saved execution status. | All six local notebooks reviewed; all have execution counts on every code cell and no saved errors. Fresh execution pending. |
| 2026-09-20 | Added Research 06: weighted MaxCut across classical methods, Qiskit/Qrisp, OpenQARP, and IBM/IQM noise models, with optional hardware cells. | [Local validation](reports/research06/VALIDATION.md): 25 simulator runs, circuit equivalence checks, clean dependency check, and offline job-recovery tests passed. Colab and hardware execution pending. |
| 2026-09-20 | Split Research 06 hardware configuration into independent IBM and IQM cells, added both IBM Secret-name pairs and the Qrisp IQM measurement example. | Full local notebook rerun, independent-connection mock tests, job-ledger regression tests, and dependency checks passed. Live accounts and hardware not tested. |

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
