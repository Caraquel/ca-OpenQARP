# Research brief — portable weighted MaxCut benchmark

## Improved prompt

Create a self-contained Google Colab research notebook that extends the OpenQARP
tutorials into a reproducible portfolio case study. Use weighted MaxCut to model
splitting conflicting tasks into two groups. Label the small input graph as a
synthetic demonstration, not a production dataset.

Install a compatible, pinned combination of Qiskit, Qiskit Aer, IBM Runtime,
IQM Client's Qiskit integration, Qrisp, and Fujitsu OpenQARP. Solve the problem
classically with exhaustive enumeration and a seeded local-search heuristic.
Train a small QAOA circuit against an independent NumPy reference, then freeze
its parameters and evaluate the same circuit on ideal Aer, Qrisp-generated
circuits on Aer, OpenQARP, an IBM device-noise simulator, and an IQM device-noise
simulator. Qrisp is a circuit-building framework, not a separate QPU vendor.

Verify objective signs, parameter conventions, bit order, and cross-framework
agreement. Use repeated seeds, equal shot budgets, warm-up runs, and a fixed
transpiler seed. Report expected cut value, approximation ratio, optimum-hit
probability, sampling uncertainty, distance from the ideal distribution, circuit
depth, two-qubit gates, and separate preparation and execution timings. Preserve
raw counts, optimizer history, problem definition, parameters, package versions,
and figures in an exportable results bundle.

Provide optional IBM and IQM hardware connection, circuit-review, submission,
and retrieval cells. Reuse existing authenticated objects or saved accounts when
available; otherwise use configurable environment/Colab Secret names. Never
embed credentials or submit hardware jobs during the default run. Keep remote
queue-inclusive timings separate from local simulator timings. Save job IDs
immediately and prevent accidental resubmission for the same experiment.

Include research exercises, methodological limitations, an honest portfolio
write-up template, and primary documentation links. Update the project README
with the new notebook and its actual validation status. Do not claim quantum
advantage from a small classical simulation or rank hardware providers using
different bundled noise snapshots.

## Design decisions

- Five weighted vertices fit both the bundled IBM Manila and IQM Adonis models.
- Train once with three seeded starts; freeze angles before comparing backends.
- Separate optimization quality from execution fidelity. Local-search timing and
  simulation timing are different workloads, not evidence of quantum speedup.
- Real hardware is an optional fixed-circuit evaluation, not a costly remote
  optimization loop.
- Reuse the user's Colab Secrets: `IBM_TOKEN` / `IBM_CRN`, or the earlier
  `IBM_QUANTUM_TOKEN` / `IBM_QUANTUM_CRN` pair, and `IQM_API_TOKEN`.
  IBM and IQM connections are in independent notebook cells. Device names and the IQM endpoint are
  configurable, and existing authenticated objects can be reused. Live account
  access and hardware execution require the user's runtime.

## Primary references

- [OpenQARP documentation](https://docs.openqarp.com/)
- [IBM local testing and device-noise models](https://quantum.cloud.ibm.com/docs/en/guides/local-testing-mode)
- [IBM Runtime service](https://docs.quantum.ibm.com/api/qiskit-ibm-runtime/runtime-service)
- [IQM Qiskit integration, simulation, and authentication](https://docs.iqm.tech/iqm-client/user_guide_qiskit.html)
- [Qrisp tutorial and circuit export](https://qrisp.eu/general/tutorial/tutorial.html)

Dependency metadata reviewed on 2026-09-20: IQM Client 35.0.3's Qiskit extra
requires Qiskit below 2.2, while IBM Runtime 0.49.0 requires Qiskit at least 2.3.
The notebook therefore uses Qiskit 2.1.2 and IBM Runtime 0.41.1, with modern
SamplerV2 hardware calls, rather than installing all packages at their latest
versions. Revalidate the complete environment before upgrading pins.
