#!/usr/bin/env python3
"""
03_corpus_profile.py
====================
Descriptive profile of the merged corpus for Section 3 reporting: document
types (harmonised across Scopus/WoS vocabularies), top publication venues
(with the split Lecture-Notes labels combined), and language distribution.

Writes count tables (CSV) plus one supplementary figure with the numbers
printed on the bars, so the figure can be read directly or cited alongside the
tables. No figure title (captions are added manually in the manuscript).

Outputs (ConnversationalRSs/outputs/):
  - corpus_profile_doctypes_<date>.csv
  - corpus_profile_venues_<date>.csv
  - corpus_profile_language_<date>.csv
  - figures/fig_corpus_profile_<date>.png   (doc types + top venues, labelled)

Deterministic; no randomness.
"""
from __future__ import annotations
import sys
from datetime import date
from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).resolve().parent))
from runlog import log_run

# ----------------------------------------------------------------------------
BASE_DIR = Path("ConnversationalRSs")
OUT_DIR  = BASE_DIR / "outputs"
FIG_DIR  = OUT_DIR / "figures"
MERGED_FILE = None            # None -> newest merged_scopus_wos_*.csv
TOP_VENUES = 12
RUN_DATE = date.today().isoformat()

# harmonise the two databases' document-type vocabularies into shared buckets
DOCTYPE_MAP = {
    "Conference paper": "Conference",
    "Proceedings Paper": "Conference",
    "Conference review": "Conference",
    "Article; Proceedings Paper": "Conference",
    "Article": "Journal article",
    "Article; Book Chapter": "Journal article",
    "Review": "Review",
    "Book chapter": "Book chapter",
    "Editorial": "Other", "Erratum": "Other", "Correction": "Other", "Note": "Other",
}
DOCTYPE_ORDER = ["Conference", "Journal article", "Review", "Book chapter", "Other"]

# collapse venue-name variants that denote the same outlet
VENUE_CANON = {
    "Lecture Notes in Computer Science (including subseries Lecture Notes in "
    "Artificial Intelligence and Lecture Notes in Bioinformatics)":
        "Lecture Notes in Computer Science",
}
# short labels for the figure only (full names kept in the CSV)
VENUE_SHORT = {
    "Lecture Notes in Computer Science": "LNCS",
    "CEUR Workshop Proceedings": "CEUR Workshop Proc.",
    "ACM International Conference Proceeding Series": "ACM ICPS",
    "International Conference on Information and Knowledge Management, Proceedings": "CIKM",
    "Proceedings of the ACM SIGKDD International Conference on Knowledge Discovery and Data Mining": "ACM SIGKDD",
    "Proceedings of the Annual Meeting of the Association for Computational Linguistics": "ACL",
    "ACM Transactions on Information Systems": "ACM TOIS",
    "IEEE Transactions on Knowledge and Data Engineering": "IEEE TKDE",
}
# ----------------------------------------------------------------------------


def find_merged():
    if MERGED_FILE:
        return Path(MERGED_FILE)
    c = sorted(OUT_DIR.glob("merged_scopus_wos_*.csv"))
    if not c:
        sys.exit(f"ERROR: no merged_scopus_wos_*.csv in {OUT_DIR}")
    return c[-1]


def main():
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(find_merged(), dtype=str, encoding="utf-8-sig", keep_default_na=False)

    # ---- language ---------------------------------------------------------
    lang = (df["Language of Original Document"].str.strip().replace("", "(unspecified)")
            .value_counts())
    lang.rename_axis("language").reset_index(name="records").to_csv(
        OUT_DIR / f"corpus_profile_language_{RUN_DATE}.csv", index=False)

    # ---- document types (harmonised) -------------------------------------
    dt = df["Document Type"].str.strip()
    dt_bucket = dt.map(lambda x: DOCTYPE_MAP.get(x, "Other"))
    dt_counts = dt_bucket.value_counts().reindex(DOCTYPE_ORDER, fill_value=0)
    dt_counts.rename_axis("document_type").reset_index(name="records").to_csv(
        OUT_DIR / f"corpus_profile_doctypes_{RUN_DATE}.csv", index=False)

    # ---- venues (canonicalised) ------------------------------------------
    ven = (df["Source title"].str.strip().replace("", "(unspecified)")
           .map(lambda x: VENUE_CANON.get(x, x)))
    ven_counts = ven.value_counts().head(TOP_VENUES)
    ven_counts.rename_axis("venue").reset_index(name="records").to_csv(
        OUT_DIR / f"corpus_profile_venues_{RUN_DATE}.csv", index=False)

    # ---- figure: doc types (left) + top venues (right), labelled ---------
    fig, (axL, axR) = plt.subplots(1, 2, figsize=(12, 5.2),
                                   gridspec_kw={"width_ratios": [1, 1.5]})

    # doc types
    dvals = dt_counts[::-1]
    axL.barh(range(len(dvals)), dvals.values, color="#4c78a8")
    axL.set_yticks(range(len(dvals))); axL.set_yticklabels(dvals.index)
    axL.set_xlabel("Records")
    for i, v in enumerate(dvals.values):
        axL.text(v + max(dvals.values) * 0.01, i, str(int(v)), va="center", fontsize=9)
    axL.set_xlim(0, max(dvals.values) * 1.12)

    # top venues (short labels)
    vlabels = [VENUE_SHORT.get(x, (x[:32] + "…") if len(x) > 33 else x)
               for x in ven_counts.index][::-1]
    vvals = ven_counts.values[::-1]
    axR.barh(range(len(vvals)), vvals, color="#72b7b2")
    axR.set_yticks(range(len(vvals))); axR.set_yticklabels(vlabels, fontsize=9)
    axR.set_xlabel("Records")
    for i, v in enumerate(vvals):
        axR.text(v + max(vvals) * 0.01, i, str(int(v)), va="center", fontsize=9)
    axR.set_xlim(0, max(vvals) * 1.12)

    plt.tight_layout()
    fig_path = FIG_DIR / f"fig_corpus_profile_{RUN_DATE}.png"
    plt.savefig(fig_path, dpi=150); plt.close()

    # ---- console summary --------------------------------------------------
    n = len(df)
    n_en = int(lang.get("English", 0))
    print("Corpus profile built.")
    print(f"  records: {n} | English: {n_en} | non-English: {n - n_en - int(lang.get('(unspecified)',0))}")
    print(f"  document types: {dict(dt_counts)}")
    print(f"  top venue: {ven_counts.index[0]} ({int(ven_counts.iloc[0])})")
    print(f"  figure -> {fig_path}")

    log = log_run(__file__,
                  inputs=[str(find_merged())],
                  outputs=[str(fig_path),
                           str(OUT_DIR / f"corpus_profile_doctypes_{RUN_DATE}.csv"),
                           str(OUT_DIR / f"corpus_profile_venues_{RUN_DATE}.csv"),
                           str(OUT_DIR / f"corpus_profile_language_{RUN_DATE}.csv")],
                  notes=f"{n} records; English {n_en}; conference "
                        f"{int(dt_counts['Conference'])}, article {int(dt_counts['Journal article'])}")
    print(f"  run log -> {log}")


if __name__ == "__main__":
    main()
