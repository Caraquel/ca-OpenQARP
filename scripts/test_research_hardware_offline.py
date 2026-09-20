"""Exercise notebook job-ledger/retrieval logic with mocks, never cloud accounts."""
import json
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
from unittest.mock import patch

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
nb = json.loads((ROOT / "OpenQARP_Research_06_MultiProvider_MaxCut_Colab.ipynb").read_text(encoding="utf-8"))
sources = ["".join(c["source"]) for c in nb["cells"] if c["cell_type"] == "code"]
submit = next(s for s in sources if s.startswith("# Submission is separate"))
retrieve = next(s for s in sources if s.startswith("HARDWARE_ROWS ="))
# Enable the notebook's explicit toggles only inside this mocked test.
submit = submit.replace('SUBMIT_IBM = False', 'SUBMIT_IBM = True').replace('SUBMIT_IQM = False', 'SUBMIT_IQM = True')
retrieve = retrieve.replace('FETCH_HARDWARE_RESULTS = False', 'FETCH_HARDWARE_RESULTS = True')


class Job:
    def __init__(self, provider):
        self.provider = provider

    def job_id(self):
        return "offline-test-" + self.provider

    def result(self, timeout):
        if self.provider == "IBM":
            return [SimpleNamespace(data=SimpleNamespace(meas=SimpleNamespace(get_counts=lambda: {"00101": 64}))) for _ in range(2)]
        return SimpleNamespace(get_counts=lambda index: {"00101": 64})


class Backend:
    def __init__(self, provider):
        self.provider, self.name, self.submissions = provider, "offline-" + provider, 0

    def run(self, circuits, shots):
        assert len(circuits) == 2 and shots == 64
        self.submissions += 1
        return Job(self.provider)

    def retrieve_job(self, job_id):
        assert job_id == "offline-test-" + self.provider
        return Job(self.provider)


class Circuit:
    layout = "offline layout"

    def copy(self):
        return self


class Sampler:
    def __init__(self, mode):
        self.backend = mode

    def run(self, circuits, shots):
        return self.backend.run(circuits, shots)


def counts_vector(raw):
    result = np.zeros(32, dtype=int)
    for key, count in raw.items():
        result[int(key, 2)] = count
    return result


with TemporaryDirectory(dir=ROOT / "Ignore_folder") as directory:
    backends = {p: Backend(p) for p in ["IBM", "IQM"]}
    scope = dict(json=json, np=np, LEDGER_PATH=Path(directory) / "ledger.json",
                 SUBMIT_IBM=True, SUBMIT_IQM=True, FETCH_HARDWARE_RESULTS=True,
                 HARDWARE={p: dict(backend=b, circuit=Circuit()) for p, b in backends.items()},
                 HARDWARE_SHOTS=64, HARDWARE_REPETITIONS=2, EXPERIMENT_ID="offline",
                 THETA=np.array([0.1, 0.2]), circuit_stats=lambda circuit: {"depth": 1},
                 counts_vector=counts_vector, score_counts=lambda counts: {"shots": int(counts.sum())},
                 LABELS=[format(i, "05b")[::-1] for i in range(32)],
                 pd=SimpleNamespace(DataFrame=lambda rows: rows), display=lambda value: None,
                 ibm_service=SimpleNamespace(job=backends["IBM"].retrieve_job))
    with patch("qiskit_ibm_runtime.SamplerV2", Sampler):
        exec(compile(submit, "submission-cell", "exec"), scope)
        assert all(b.submissions == 1 for b in backends.values())
        exec(compile(submit, "submission-cell", "exec"), scope)
        assert all(b.submissions == 1 for b in backends.values()), "Duplicate submission was not blocked"
        # Simulate a new session: retrieve from job IDs, not in-memory Job objects.
        scope["LIVE_JOBS"] = {}
        exec(compile(retrieve, "retrieval-cell", "exec"), scope)
        assert len(scope["HARDWARE_ROWS"]) == 4
        saved = json.loads(scope["LEDGER_PATH"].read_text())
        assert all(r["status"] == "retrieved" for r in saved.values())
        assert saved["IBM"]["counts_q0_first"]["0"] == {"10100": 64}
        # An interrupted network submission must also block retries.
        scope["LEDGER_PATH"].write_text(json.dumps({"IBM": {"status": "submission_started"}}))
        exec(compile(submit.replace('SUBMIT_IQM = True', 'SUBMIT_IQM = False'), "submission-cell", "exec"), scope)
        assert backends["IBM"].submissions == 1
        # Changed angles must not silently mix a prior hardware experiment into results.
        scope["LEDGER_PATH"].write_text(json.dumps(saved))
        scope["THETA"] = np.array([0.3, 0.4])
        try:
            exec(compile(retrieve, "retrieval-cell", "exec"), scope)
        except AssertionError as error:
            assert "angles differ" in str(error)
        else:
            raise AssertionError("Mismatched hardware angles were accepted")
print("PASS: mock submission, duplicate/interrupted guards, job recovery, count ordering, and angle matching.")
