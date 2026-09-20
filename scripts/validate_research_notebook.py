"""Execute the local-only research notebook in the current pinned environment.

Usage: path/to/benchmark-env/python scripts/validate_research_notebook.py
Install the notebook's dependency pins before invoking this script.
"""
import json
import os
from pathlib import Path
import sys

import nbformat
from nbclient import NotebookClient

ROOT = Path(__file__).resolve().parents[1]
notebook_path = ROOT / "OpenQARP_Research_06_MultiProvider_MaxCut_Colab.ipynb"
nb = nbformat.read(notebook_path, as_version=4)
nbformat.validate(nb)
for cell in nb.cells:
    if cell.cell_type == "code":
        compile(cell.source, str(notebook_path), "exec")

# Keep the kernel registration local to this ignored testing directory.
jupyter_root = ROOT / "Ignore_folder" / "benchmark-jupyter"
kernel_dir = jupyter_root / "kernels" / "benchmark"
kernel_dir.mkdir(parents=True, exist_ok=True)
(kernel_dir / "kernel.json").write_text(json.dumps({
    "argv": [sys.executable, "-m", "ipykernel_launcher", "-f", "{connection_file}"],
    "display_name": "Benchmark validation", "language": "python",
}))
os.environ["JUPYTER_PATH"] = str(jupyter_root)
os.environ["MPLBACKEND"] = "module://matplotlib_inline.backend_inline"
os.chdir(ROOT)
client = NotebookClient(nb, timeout=300, kernel_name="benchmark",
                        skip_cells_with_tag="installation", allow_errors=False)
client.on_cell_start = lambda cell, cell_index: print(f"Cell {cell_index}: {cell.cell_type}", flush=True)
try:
    client.execute(cwd=str(ROOT))
finally:
    nbformat.write(nb, ROOT / "Ignore_folder" / "research06.executed.ipynb")
print("Notebook executed successfully; hardware and installation cells were not run.")
