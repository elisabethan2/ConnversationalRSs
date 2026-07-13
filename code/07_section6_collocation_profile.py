#!/usr/bin/env python3
"""
07_section6_collocation_profile.py
==================================
Section 6, "presence" figure: what the conversation-family node words actually
keep company with. Pairs with the gradient-of-absence figure (04): the gradient
shows the interactional vocabulary that is NOT there; this shows the
instrumental vocabulary that IS.

Reads the register-test output (no engine re-run needed):
    ConnversationalRSs/outputs/register_hits_<date>.csv
        columns: record, year, band, node, collocate, register, title

Outputs (date-stamped):
    ConnversationalRSs/outputs/colloc_profile_<date>.csv          ranked counts
    ConnversationalRSs/outputs/figures/fig_colloc_profile_<date>.png

Metric (default = records): number of DISTINCT records in which a collocate
occurs near a conversation-family node word. Record counts are more defensible
than raw instance counts for the claim "in N records, conversation collocates
with X"; pass --metric instances for token counts instead.

By default the script is faithful to register_hits and does NOT merge
morphological variants (so 'preference' and 'preferences' stay separate). To
merge them, populate COLLAPSE below; the mapping used is printed and logged.

Deterministic: no randomness, so no seed is required.
"""
from __future__ import annotations
import sys, argparse
from datetime import date
from pathlib import Path
import pandas as pd

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).resolve().parent))
try:
    from runlog import log_run
except Exception:
    log_run = None

# ---------------------------------------------------------------- CONFIG -----
BASE_DIR = Path("ConnversationalRSs")
OUT_DIR  = BASE_DIR / "outputs"
FIG_DIR  = OUT_DIR / "figures"
RUN_DATE = date.today().isoformat()

TOP_N = 15
BAR_COLOR = "#4c78a8"          # single colour: these are all one register

# Optional morphological merge. Empty = faithful to register_hits.
# To collapse families, map each surface form to a canonical label, e.g.:
#   "preferences": "preference", "modeling": "model", "learn": "learning"
#COLLAPSE: dict[str, str] = {}
COLLAPSE = {"modeling": "model", "learn": "learning", "elicitation": "elicit",}

def find_hits(explicit: str | None) -> Path:
    if explicit:
        p = Path(explicit)
        if not p.exists():
            sys.exit(f"ERROR: hits file not found: {p}")
        return p
    cands = sorted(OUT_DIR.glob("register_hits_*.csv"))
    if not cands:
        sys.exit(f"ERROR: no register_hits_*.csv in {OUT_DIR}")
    return cands[-1]


def build_profile(hits: pd.DataFrame, register: str, metric: str) -> tuple[pd.DataFrame, int]:
    d = hits[hits["register"] == register].copy()
    d["collocate"] = d["collocate"].map(lambda c: COLLAPSE.get(c, c))
    n_records_base = d["record"].nunique()
    if metric == "records":
        prof = (d.groupby("collocate")["record"].nunique()
                .sort_values(ascending=False).rename("count").reset_index())
    else:  # instances
        prof = (d.groupby("collocate").size()
                .sort_values(ascending=False).rename("count").reset_index())
    prof.insert(0, "rank", range(1, len(prof) + 1))
    return prof, n_records_base


def make_figure(prof: pd.DataFrame, n_base: int, metric: str, top_n: int, path: Path) -> None:
    top = prof.head(top_n).iloc[::-1]          # reverse so largest sits at top
    fig, ax = plt.subplots(figsize=(8, 0.42 * len(top) + 1.2))
    ax.barh(top["collocate"], top["count"], color=BAR_COLOR, height=0.68)
    for y, v in enumerate(top["count"]):
        ax.text(v, y, f" {int(v)}", va="center", ha="left", fontsize=9)
    unit = (f"records (of {n_base} with a conversation-family collocate)"
            if metric == "records" else "collocate tokens")
    ax.set_xlabel(f"Instrumental collocates by {unit}")
    ax.set_xlim(0, top["count"].max() * 1.12)
    ax.spines[["top", "right"]].set_visible(False)
    ax.margins(y=0.01)
    plt.tight_layout()
    plt.savefig(path, dpi=150)
    plt.close()


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--hits", default=None, help="path to a specific register_hits CSV")
    ap.add_argument("--outdir", default=None)
    ap.add_argument("--figdir", default=None)
    ap.add_argument("--metric", choices=["records", "instances"], default="records")
    ap.add_argument("--top", type=int, default=TOP_N)
    ap.add_argument("--register", default="instrumental")
    args = ap.parse_args()

    hits_path = find_hits(args.hits)
    outdir = Path(args.outdir) if args.outdir else OUT_DIR
    figdir = Path(args.figdir) if args.figdir else FIG_DIR
    outdir.mkdir(parents=True, exist_ok=True)
    figdir.mkdir(parents=True, exist_ok=True)

    hits = pd.read_csv(hits_path)
    prof, n_base = build_profile(hits, args.register, args.metric)

    csv_path = outdir / f"colloc_profile_{RUN_DATE}.csv"
    fig_path = figdir / f"fig_colloc_profile_{RUN_DATE}.png"
    prof.to_csv(csv_path, index=False)
    make_figure(prof, n_base, args.metric, args.top, fig_path)

    print(f"  hits read   <- {hits_path}")
    print(f"  register    =  {args.register}   metric = {args.metric}")
    print(f"  collapse map=  {COLLAPSE or 'none (faithful to register_hits)'}")
    print(f"  base records=  {n_base}")
    print(f"  profile csv -> {csv_path}")
    print(f"  figure      -> {fig_path}")
    print(f"\n  top {args.top} instrumental collocates:")
    print(prof.head(args.top).to_string(index=False))

    if log_run is not None:
        log = log_run(
            __file__,
            inputs=[str(hits_path)],
            outputs=[str(csv_path), str(fig_path)],
            params=f"register={args.register}, metric={args.metric}, top={args.top}, "
                   f"collapse={COLLAPSE or 'none'}",
            notes=f"base_records={n_base}; deterministic (no randomness)",
        )
        print(f"  run log -> {log}")


if __name__ == "__main__":
    main()
