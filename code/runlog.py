"""
runlog.py  --  shared run-logging helper for the ConnversationalRSs project.

Call log_run(...) at the end of any analysis script. It appends a timestamped,
environment-stamped entry to docs/run_log.md so every run is reproducibly
documented: inputs, outputs, parameters, package versions, and (if available)
the git commit the code was at.

Usage in a script:
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from runlog import log_run
    ...
    log_run(__file__,
            inputs=[str(infile)],
            outputs=[str(fig), str(table)],
            params="min_occ=5, resolution=0.6",
            notes="866 records; peak 2025")
"""
from __future__ import annotations
import platform, subprocess, importlib
from datetime import datetime
from pathlib import Path

# packages worth recording if they happen to be installed/used
_PKGS = ["pandas", "numpy", "matplotlib", "scipy", "scikit-learn", "sklearn",
         "networkx", "nltk", "spacy", "gensim", "bertopic",
         "sentence_transformers", "openpyxl", "xlrd"]

# default run log location (project docs folder)
DEFAULT_LOG = Path("ConnversationalRSs/docs/run_log.md")


def _versions() -> str:
    parts = [f"python {platform.python_version()}"]
    seen = set()
    for name in _PKGS:
        mod = name if name != "scikit-learn" else "sklearn"
        if mod in seen:
            continue
        try:
            m = importlib.import_module(mod)
            parts.append(f"{mod} {getattr(m, '__version__', '?')}")
            seen.add(mod)
        except Exception:
            pass
    return " | ".join(parts)


def _git_hash(start: Path) -> str:
    try:
        r = subprocess.run(["git", "-C", str(start), "rev-parse", "--short", "HEAD"],
                           capture_output=True, text=True, timeout=5)
        if r.returncode == 0 and r.stdout.strip():
            dirty = subprocess.run(["git", "-C", str(start), "status", "--porcelain"],
                                   capture_output=True, text=True, timeout=5)
            flag = " (uncommitted changes)" if dirty.stdout.strip() else ""
            return r.stdout.strip() + flag
    except Exception:
        pass
    return "(not a git repo / git unavailable)"


def log_run(script, inputs=None, outputs=None, params=None, notes=None, log_path=None) -> Path:
    """Append a markdown run-log entry. Returns the log file path."""
    log_path = Path(log_path) if log_path else DEFAULT_LOG
    log_path.parent.mkdir(parents=True, exist_ok=True)

    def _fmt(x):
        if not x:
            return "  - (none)"
        if isinstance(x, (str, Path)):
            x = [x]
        return "\n".join(f"  - {i}" for i in x)

    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = [
        f"## {ts} — {Path(str(script)).name}",
        f"- git: {_git_hash(log_path.parent)}",
        f"- inputs:\n{_fmt(inputs)}",
        f"- outputs:\n{_fmt(outputs)}",
    ]
    if params:
        entry.append(f"- params: {params}")
    if notes:
        entry.append(f"- notes: {notes}")
    entry.append(f"- env: {_versions()}")
    entry.append("\n---\n")

    with log_path.open("a", encoding="utf-8") as f:
        f.write("\n".join(entry) + "\n")
    return log_path
