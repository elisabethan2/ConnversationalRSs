#!/usr/bin/env python3
"""
02_emergence_curve.py
=====================
Figure 1 for the term-mapping paper: the publication-per-year "emergence curve"
for the "conversational recommend*" corpus, with each year's bar split by
provenance (Scopus-only / both / WoS-only) so growth and cross-database
coverage are visible in one figure.

Reads the merged corpus produced by 01_merge_scopus_wos.py and writes:
  - figures/fig1_emergence_curve_<date>.png   the figure
  - fig1_emergence_data_<date>.csv            the year x source_db counts
                                              behind the figure (for transparency)

The final (current) year is hatched and labelled because it is a PARTIAL year.

Deterministic; no randomness, so no seed required.
"""
from __future__ import annotations
import sys, platform
from datetime import date, datetime
from pathlib import Path

import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).resolve().parent))
from runlog import log_run

# ----------------------------------------------------------------------------
# CONFIG -- set BASE_DIR to the absolute project path if you run from elsewhere.
# (Folder spelling 'ConnversationalRSs' as provided; correct if it was a typo.)
# ----------------------------------------------------------------------------
BASE_DIR = Path("ConnversationalRSs")
OUT_DIR  = BASE_DIR / "outputs"
FIG_DIR  = OUT_DIR / "figures"

MERGED_FILE = None              # None -> newest merged_scopus_wos_*.csv in OUT_DIR
PARTIAL_YEAR = 2026             # render/label this year as incomplete
RUN_DATE = date.today().isoformat()

# stack order + colours (Scopus primary at base)
SOURCE_ORDER  = ["scopus", "both", "wos"]
SOURCE_LABELS = {"scopus": "Scopus only", "both": "Scopus & WoS", "wos": "WoS only"}
SOURCE_COLORS = {"scopus": "#1f77b4", "both": "#6a51a3", "wos": "#d62728"}
# ----------------------------------------------------------------------------


def find_merged() -> Path:
    if MERGED_FILE:
        return Path(MERGED_FILE)
    cands = sorted(OUT_DIR.glob("merged_scopus_wos_*.csv"))
    if not cands:
        sys.exit(f"ERROR: no merged_scopus_wos_*.csv in {OUT_DIR}. Run 01_merge_scopus_wos.py first.")
    return cands[-1]


def main():
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    merged = find_merged()
    df = pd.read_csv(merged, dtype=str, encoding="utf-8-sig", keep_default_na=False)
    for col in ("Year", "source_db"):
        if col not in df.columns:
            sys.exit(f"ERROR: merged file lacks '{col}' column.")

    df["yr"] = pd.to_numeric(df["Year"], errors="coerce")
    df = df.dropna(subset=["yr"]).astype({"yr": int})

    # year x source_db count matrix
    pivot = (df.groupby(["yr", "source_db"]).size().unstack(fill_value=0)
             .reindex(columns=SOURCE_ORDER, fill_value=0).sort_index())
    full_years = range(int(pivot.index.min()), int(pivot.index.max()) + 1)
    pivot = pivot.reindex(full_years, fill_value=0)
    pivot.to_csv(OUT_DIR / f"fig1_emergence_data_{RUN_DATE}.csv")

    # ---- plot stacked bars ------------------------------------------------
    fig, ax = plt.subplots(figsize=(9, 4.8))
    bottom = pd.Series(0, index=pivot.index)
    for src in SOURCE_ORDER:
        vals = pivot[src]
        bars = ax.bar(pivot.index, vals, bottom=bottom,
                      color=SOURCE_COLORS[src], label=SOURCE_LABELS[src], width=0.8)
        # hatch the partial year segment
        for b, yr in zip(bars, pivot.index):
            if yr == PARTIAL_YEAR:
                b.set_hatch("////"); b.set_edgecolor("white")
        bottom = bottom + vals

    totals = pivot.sum(axis=1)
    if PARTIAL_YEAR in totals.index:
        ax.annotate(f"{PARTIAL_YEAR} partial\n(through export date)",
                    xy=(PARTIAL_YEAR, totals[PARTIAL_YEAR]),
                    xytext=(0, 10), textcoords="offset points",
                    ha="center", va="bottom", fontsize=8, color="#555")

    ax.set_xlabel("Publication year")
    ax.set_ylabel("Publications")
    ax.set_title('Emergence of "conversational recommend*" (Scopus + Web of Science)')
    ax.set_xticks(list(pivot.index))
    ax.set_xticklabels([str(y) for y in pivot.index], rotation=45, ha="right", fontsize=8)
    ax.legend(frameon=False)
    ax.grid(axis="y", alpha=.3)
    plt.tight_layout()
    fig_path = FIG_DIR / f"fig1_emergence_curve_{RUN_DATE}.png"
    plt.savefig(fig_path, dpi=150)
    plt.close()

    # ---- console summary --------------------------------------------------
    n = len(df)
    pct_2020 = 100 * (df["yr"] >= 2020).mean()
    peak_year = int(totals.idxmax())
    print("Emergence curve built.")
    print(f"  records with a year: {n}")
    print(f"  year range: {int(pivot.index.min())}-{int(pivot.index.max())}")
    print(f"  share 2020+: {pct_2020:.0f}%")
    print(f"  peak year: {peak_year} ({int(totals[peak_year])} records)")
    print(f"  figure -> {fig_path}")
    print(f"  data   -> {OUT_DIR / f'fig1_emergence_data_{RUN_DATE}.csv'}")
    print(f"  env: python {platform.python_version()}, pandas {pd.__version__}, "
          f"matplotlib {matplotlib.__version__}  ({datetime.now():%Y-%m-%d %H:%M})")

    data_path = OUT_DIR / f"fig1_emergence_data_{RUN_DATE}.csv"
    log = log_run(__file__,
                  inputs=[str(merged)],
                  outputs=[str(fig_path), str(data_path)],
                  params=f"PARTIAL_YEAR={PARTIAL_YEAR}",
                  notes=f"{n} records; {pct_2020:.0f}% 2020+; peak {peak_year}")
    print(f"  run log -> {log}")


if __name__ == "__main__":
    main()
