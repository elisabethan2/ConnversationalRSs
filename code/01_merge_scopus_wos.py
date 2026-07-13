#!/usr/bin/env python3
"""
01_merge_scopus_wos.py
======================
Merge a Scopus export (CSV) and a Web of Science export (tab-delimited, one or
more files) for the SAME query into a single, de-duplicated corpus for the
"conversational recommender systems" term study.

WHY THIS SCRIPT EXISTS (for the methods section)
------------------------------------------------
Scopus and WoS overlap heavily but not completely, and they use different
schemas (Scopus = human-readable column names + EID; WoS = two-letter field
tags + UT). To analyse the union reproducibly we must:
  1. map both into ONE common schema (we use the Scopus column layout, so the
     output also loads directly in VOSviewer's *Scopus* import tab and in any
     downstream Scopus-shaped scripts),
  2. de-duplicate ACROSS databases on a stable key (normalized DOI first, then
     normalized title + year for the records lacking a DOI),
  3. tag every surviving record's provenance as scopus / wos / both, so the
     overlap is a reported number, not a hidden tool guess.

DESIGN DECISIONS (documented, change deliberately)
--------------------------------------------------
- On a record present in BOTH databases we keep the SCOPUS copy as primary
  (richer/*consistent* subject + reference formatting for the Scopus parser)
  and record that WoS also held it (wos_UT, source_db='both').
- "Cited by" for a 'both' record is the Scopus count; WoS "Times Cited" differs
  (different citation universe) and is NOT substituted.
- References are carried in each record's NATIVE format and flagged in
  `ref_format` (scopus|wos). IMPORTANT: because Scopus and WoS reference STRING
  formats differ, this merged file is reliable for KEYWORD / DESCRIPTIVE maps
  but NOT for cross-database co-citation / bibliographic coupling. Run those
  citation analyses PER DATABASE (one Scopus file, one WoS file) and compare.

The script READS the raw exports only; it never modifies them. Output filename
is date-stamped so a re-run never overwrites a prior union. Fully deterministic
(sorted output); no randomness, so no seed required.
"""
from __future__ import annotations
import sys, re, platform
from datetime import date, datetime
from pathlib import Path

import pandas as pd
import csv as _csv

sys.path.insert(0, str(Path(__file__).resolve().parent))
from runlog import log_run

# ----------------------------------------------------------------------------
# CONFIG  -- set BASE_DIR to the absolute path of the project root if you run
# from elsewhere. (Note the folder spelling: 'ConnversationalRSs' as provided;
# correct here if that was a typo.)
# ----------------------------------------------------------------------------
BASE_DIR = Path("ConnversationalRSs")
DATA_DIR = BASE_DIR / "data"            # immutable raw exports live here
OUT_DIR  = BASE_DIR / "outputs"         # derived union + provenance report

SCOPUS_GLOB = "scopus_export*.csv"      # the Scopus CSV
WOS_GLOB    = "savedrecs*.txt"          # one or more WoS tab-delimited files

RUN_DATE = date.today().isoformat()
OUT_FILE   = None                       # default set below (date-stamped)
REPORT_FILE = None
# ----------------------------------------------------------------------------

# Full Scopus column order (the common/output schema).
SCOPUS_COLS = [
    "Authors", "Author full names", "Author(s) ID", "Title", "Year",
    "Source title", "Volume", "Issue", "Art. No.", "Page start", "Page end",
    "Cited by", "DOI", "Link", "Affiliations", "Authors with affiliations",
    "Abstract", "Author Keywords", "Index Keywords", "References",
    "Correspondence Address", "Editors", "Publisher", "Sponsors",
    "Conference name", "Conference date", "Conference location",
    "Conference code", "ISSN", "ISBN", "CODEN", "PubMed ID",
    "Language of Original Document", "Abbreviated Source Title",
    "Document Type", "Publication Stage", "Open Access", "Source", "EID",
]
# WoS field tag -> Scopus column.
WOS_TO_SCOPUS = {
    "AU": "Authors", "AF": "Author full names", "TI": "Title", "PY": "Year",
    "SO": "Source title", "VL": "Volume", "IS": "Issue", "AR": "Art. No.",
    "BP": "Page start", "EP": "Page end", "TC": "Cited by", "DI": "DOI",
    "AB": "Abstract", "DE": "Author Keywords", "ID": "Index Keywords",
    "CR": "References", "PU": "Publisher", "SN": "ISSN", "BN": "ISBN",
    "PM": "PubMed ID", "LA": "Language of Original Document",
    "J9": "Abbreviated Source Title", "DT": "Document Type",
    "CT": "Conference name", "CY": "Conference date", "CL": "Conference location",
}
# Extra provenance / traceability columns appended to the output.
EXTRA_COLS = ["source_db", "dedup_method", "wos_UT", "WoS Categories",
              "Research Areas", "ref_format"]


def _one(glob_pat):
    hits = sorted(DATA_DIR.glob(glob_pat))
    return hits


def norm_doi(s: str) -> str:
    s = (s or "").strip().lower()
    s = re.sub(r"^https?://(dx\.)?doi\.org/", "", s)
    return s.rstrip(".")


def norm_title(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", (s or "").lower()).strip()


def dedup_key(doi: str, title: str, year: str):
    d = norm_doi(doi)
    if d:
        return f"doi:{d}", "doi"
    t = norm_title(title)
    if t:
        return f"ti:{t}|{(year or '').strip()}", "title_year"
    return None, "unmatched"   # no DOI and no title -> never merged


def load_scopus() -> pd.DataFrame:
    files = _one(SCOPUS_GLOB)
    if not files:
        sys.exit(f"ERROR: no Scopus file matching {SCOPUS_GLOB} in {DATA_DIR}")
    df = pd.read_csv(files[0], dtype=str, encoding="utf-8-sig", keep_default_na=False)
    for c in SCOPUS_COLS:
        if c not in df.columns:
            df[c] = ""
    df = df[SCOPUS_COLS].copy()
    df["source_db"] = "scopus"
    df["wos_UT"] = ""
    df["WoS Categories"] = ""
    df["Research Areas"] = ""
    df["ref_format"] = df["References"].apply(lambda x: "scopus" if str(x).strip() else "")
    print(f"  Scopus: {len(df)} records  ({files[0].name})")
    return df


def load_wos() -> pd.DataFrame:
    files = _one(WOS_GLOB)
    if not files:
        sys.exit(f"ERROR: no WoS files matching {WOS_GLOB} in {DATA_DIR}")
    parts = []
    for f in files:
        d = pd.read_csv(f, sep="\t", encoding="utf-8-sig", dtype=str,
                        quoting=_csv.QUOTE_NONE, on_bad_lines="warn",
                        keep_default_na=False)
        parts.append(d)
        print(f"  WoS file: {len(d)} records  ({f.name})")
    wos = pd.concat(parts, ignore_index=True)
    if "UT" in wos.columns:
        before = len(wos)
        wos = wos.drop_duplicates("UT")
        if before != len(wos):
            print(f"  WoS: removed {before - len(wos)} duplicate UT rows across files")

    out = pd.DataFrame("", index=range(len(wos)), columns=SCOPUS_COLS)
    for tag, col in WOS_TO_SCOPUS.items():
        if tag in wos.columns:
            out[col] = wos[tag].values
    out["Source"] = "WoS"
    out["EID"] = ""
    out["source_db"] = "wos"
    out["wos_UT"] = wos["UT"].values if "UT" in wos.columns else ""
    out["WoS Categories"] = wos["WC"].values if "WC" in wos.columns else ""
    out["Research Areas"] = wos["SC"].values if "SC" in wos.columns else ""
    out["ref_format"] = out["References"].apply(lambda x: "wos" if str(x).strip() else "")
    print(f"  WoS total (deduped within WoS): {len(out)} records")
    return out


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out_file = OUT_FILE or (OUT_DIR / f"merged_scopus_wos_{RUN_DATE}.csv")
    report_file = REPORT_FILE or (OUT_DIR / f"merge_crossdb_report_{RUN_DATE}.md")

    print("Loading sources...")
    scopus = load_scopus()
    wos = load_wos()
    n_scopus, n_wos = len(scopus), len(wos)

    combined = pd.concat([scopus, wos], ignore_index=True)
    keys, methods = zip(*[dedup_key(r["DOI"], r["Title"], r["Year"])
                          for _, r in combined.iterrows()])
    combined["_key"] = keys
    combined["dedup_method"] = methods

    # records with no usable key stay unique (give each its own key)
    nokey = combined["_key"].isna()
    combined.loc[nokey, "_key"] = [f"row:{i}" for i in combined.index[nokey]]

    # provenance across the union: which databases hold each key?
    membership = combined.groupby("_key")["source_db"].agg(
        lambda s: "both" if set(s) >= {"scopus", "wos"} else next(iter(set(s))))

    # keep one row per key; prefer the Scopus copy (sort so scopus sorts first)
    combined["_pref"] = combined["source_db"].map({"scopus": 0, "wos": 1})
    combined = combined.sort_values(["_key", "_pref"], kind="stable")
    merged = combined.drop_duplicates("_key", keep="first").copy()
    merged["source_db"] = merged["_key"].map(membership)

    # On 'both' rows we keep the Scopus record, but carry the WoS-only fields
    # (UT plus the subject signal: WoS Categories, Research Areas) across, so
    # the cross-field information needed for the subfield-crossover analysis is
    # not lost for the 'both' records.
    wos_src = (combined[combined["source_db"] == "wos"]
               .drop_duplicates("_key").set_index("_key"))
    both_mask = merged["source_db"] == "both"
    for col in ["wos_UT", "WoS Categories", "Research Areas"]:
        carried = merged.loc[both_mask, "_key"].map(wos_src[col]).fillna("")
        merged.loc[both_mask, col] = carried

    merged = merged.drop(columns=["_key", "_pref"])
    merged = merged[SCOPUS_COLS + EXTRA_COLS]
    merged = merged.sort_values(["source_db", "Year", "Title"], kind="stable")

    # ---- counts ----------------------------------------------------------
    counts = merged["source_db"].value_counts()
    n_scopus_only = int(counts.get("scopus", 0))
    n_wos_only = int(counts.get("wos", 0))
    n_both = int(counts.get("both", 0))
    n_total = len(merged)
    by_method = merged["dedup_method"].value_counts().to_dict()

    merged.to_csv(out_file, index=False, encoding="utf-8-sig")

    # ---- provenance report ----------------------------------------------
    mapping_tbl = "\n".join(f"| {tag} | {col} |" for tag, col in WOS_TO_SCOPUS.items())
    report = f"""# Cross-database merge report -- {RUN_DATE}

Generated: {datetime.now().isoformat(timespec='seconds')}

## Inputs (raw, immutable)
- Scopus: {n_scopus} records (matched `{SCOPUS_GLOB}`)
- Web of Science: {n_wos} records after within-WoS de-duplication on UT
  (matched `{WOS_GLOB}`, concatenated across files)

## Output
- Union corpus: `{out_file.name}`  ({n_total} unique records, Scopus column layout)

## De-duplication
Key = normalized DOI if present, else normalized (title + year).
Title normalization: lowercase, non-alphanumeric -> space, whitespace collapsed.
On a record present in both databases the **Scopus** copy is kept as primary.

| provenance (source_db) | records |
|------------------------|--------:|
| scopus only | {n_scopus_only} |
| wos only    | {n_wos_only} |
| both        | {n_both} |
| **total unique** | **{n_total}** |

Keys resolved by: {by_method}

**Overlap reading:** {n_both} records appear in both databases; WoS adds
{n_wos_only} records not in Scopus. (Scopus contributed {n_scopus}; WoS
contributed {n_wos}; union {n_total}.)

## WoS -> Scopus field mapping
| WoS tag | Scopus column |
|---------|---------------|
{mapping_tbl}
WoS `WC` (categories) and `SC` (research areas) are carried as extra columns
(no Scopus-CSV equivalent); `UT` is carried as `wos_UT`.

## Reference / citation caveat
References are carried in each record's native format (`ref_format` = scopus|wos).
Because the two databases format reference strings differently, this union file
is suitable for keyword co-occurrence and descriptive mapping but NOT for
cross-database co-citation or bibliographic coupling. Run those PER DATABASE.

## Environment
- python: {platform.python_version()}
- pandas: {pd.__version__}
"""
    report_file.write_text(report, encoding="utf-8")

    print("\nMerge complete.")
    print(f"  scopus only: {n_scopus_only} | wos only: {n_wos_only} | both: {n_both}")
    print(f"  total unique: {n_total}")
    print(f"  union  -> {out_file}")
    print(f"  report -> {report_file}")

    log = log_run(__file__,
                  inputs=[str(p) for p in (_one(SCOPUS_GLOB) + _one(WOS_GLOB))],
                  outputs=[str(out_file), str(report_file)],
                  params="dedup: DOI then title+year; primary=Scopus on 'both'",
                  notes=f"scopus={n_scopus}, wos={n_wos} -> union {n_total} "
                        f"(scopus-only {n_scopus_only}, wos-only {n_wos_only}, both {n_both})")
    print(f"  run log -> {log}")


if __name__ == "__main__":
    main()
