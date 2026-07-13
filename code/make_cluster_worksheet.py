#!/usr/bin/env python3
"""
make_cluster_worksheet.py
-------------------------
Turn the primary VOSviewer map (min-5 / res-0.6) into a single annotatable
Markdown worksheet for the cluster-naming pass: clusters ordered oldest ->
newest, each with its terms (occurrences + per-term average year) and blank
lines to fill in the cluster NAME and what "conversational" means in it.

This is a thinking aid for Section 4 of the paper, not a publication table.
"""
from __future__ import annotations
import sys
from datetime import date
from pathlib import Path
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from runlog import log_run

# ----------------------------------------------------------------------------
BASE_DIR = Path("ConnversationalRSs")
OUT_DIR  = BASE_DIR / "outputs"
VOS_DIR  = OUT_DIR / "VOSViewerOutputFiles"
MAP_FILE = VOS_DIR / "mapMin5AuthorOccurencesRes0_6_250626.txt"
OUT_FILE = OUT_DIR / f"cluster_naming_worksheet_{date.today().isoformat()}.md"
# ----------------------------------------------------------------------------


def main():
    if not MAP_FILE.exists():
        sys.exit(f"ERROR: map file not found: {MAP_FILE}")
    df = pd.read_csv(MAP_FILE, sep="\t", dtype=str, keep_default_na=False)
    df["occ"] = pd.to_numeric(df["weight<Occurrences>"], errors="coerce")
    df["yr"]  = pd.to_numeric(df["score<Avg. pub. year>"], errors="coerce")
    df["cl"]  = pd.to_numeric(df["cluster"], errors="coerce").astype(int)

    # cluster-level weighted year, for ordering oldest -> newest
    cl_year = {}
    for c, sub in df.groupby("cl"):
        cl_year[c] = (sub.occ * sub.yr).sum() / sub.occ.sum()
    order = sorted(cl_year, key=lambda c: cl_year[c])

    lines = [
        f"# Cluster naming worksheet — min-5 / res-0.6",
        "",
        "> Fill in **Name** and **What \"conversational\" means here** for each cluster.",
        "> Clusters are ordered oldest → newest (occurrence-weighted avg year), so",
        "> reading top to bottom traces the diachronic shift.",
        f"> Source map: `{MAP_FILE.name}`",
        "",
        "## Quick orientation (all clusters, oldest → newest)",
        "",
        "| cluster | avg yr | #terms | total occ | leading terms |",
        "|--------:|-------:|------:|----------:|---------------|",
    ]
    for c in order:
        sub = df[df.cl == c].sort_values("occ", ascending=False)
        lead = ", ".join(sub.label.head(4))
        lines.append(f"| C{c} | {cl_year[c]:.1f} | {len(sub)} | "
                     f"{int(sub.occ.sum())} | {lead} |")
    lines += ["", "---", ""]

    for c in order:
        sub = df[df.cl == c].sort_values("occ", ascending=False)
        lines += [
            f"## Cluster {c} — avg year {cl_year[c]:.1f} · {len(sub)} terms · "
            f"{int(sub.occ.sum())} total occurrences",
            "",
            "**Name:** ______________________________________________",
            "",
            "**What \"conversational\" means here:** ___________________________________",
            "",
            "**Diachronic / notes:** _________________________________________________",
            "",
            "| term | occ | avg yr |",
            "|------|----:|-------:|",
        ]
        for _, r in sub.iterrows():
            yr = f"{r.yr:.0f}" if pd.notna(r.yr) else "—"
            lines.append(f"| {r.label} | {int(r.occ)} | {yr} |")
        lines += ["", "---", ""]

    OUT_FILE.write_text("\n".join(lines), encoding="utf-8")
    print(f"worksheet -> {OUT_FILE}  ({len(order)} clusters)")

    log = log_run(__file__,
                  inputs=[str(MAP_FILE)],
                  outputs=[str(OUT_FILE)],
                  params="min-5 / res-0.6 primary map",
                  notes=f"{len(order)} clusters, {len(df)} terms")
    print(f"run log -> {log}")


if __name__ == "__main__":
    main()
