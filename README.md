Reproducibility package for the distant- and close-reading study of how the
conversational-recommender-systems (CRS) literature conceptualises conversation.

## What this repository contains

- `code/` — numbered analysis scripts (run in order)
- `outputs/` — derived, date-stamped results (tables, CSVs) and `outputs/figures/`
- `config/` — the VOSviewer thesaurus used for keyword merging
- `docs/run_log.md` — inputs, outputs, and dates for each run
- `requirements.txt` — exact package versions

## VOSviewer maps (`outputs/VOSViewerOutputFiles/`)

The co-occurrence maps (Figures 2–4) and the cluster typology (Table 2) were
produced with VOSviewer (Van Eck & Waltman, 2010), a GUI tool, not by the
scripts in `code/`. This folder holds the exported maps and their underlying
network/cluster tables so the clustering can be inspected.

Filename key: `Min<n>` = minimum keyword occurrences; `Res<r>` = clustering
resolution; `keyword`/`Author` = unit of co-occurrence. Files are dated
250626 (25 June 2026). Inputs to VOSviewer: the merged corpus (not shared;
see below) and the thesaurus in `config/`.

| Paper item | File |
|---|---|
| Fig. 2 Co-occurrence overview | `Min5occurencesResolution0_6_250626.png` (or `10keywordsres1.png`) |
| Fig. 3 Overlay-by-year | `OverlayVisualizationResolution0_6_min5keywords250626.png` |
| Fig. 4 Long-tail era map | `3keywords0_7resolution250626.png` |
| Table 2 Cluster typology | `clustertable_Min5_Res0_6_250626.csv`, `clusterterms_Min5_Res0_6_250626.csv` |

## What is NOT included, and why

The raw Scopus and Web of Science exports and the merged corpus are **not**
redistributed here: they contain verbatim titles and abstracts under publisher
copyright, and the database terms of service do not permit redistribution.
The corpus can be reconstructed from the search string below; all *derived*
outputs needed to check the analysis are included.

**Corpus definition.** Records were retrieved on 25 June 2026 from Scopus and
Web of Science using the query `"conversational recommend*"` over title,
keywords, and abstract. Scripts `01`–`03` merge the two exports (deduplicated
on DOI, then normalised title + year) into the 866-record corpus.

## Canonical run

The figures and numbers reported in the paper come from the **2026-07-13** run
(spaCy `en_core_web_sm` active). Earlier dated outputs (2026-06-29, 2026-06-30)
are retained for provenance only: the 2026-06-30 run predates the model install
and the final concordance exclusions, and its `register_hits` is byte-identical
to 2026-07-13 (the model install did not change that output). When a filename
appears with several dates, use the 2026-07-13 version.

## Environment

- Python 3.13, spaCy 3.8.14, model `en_core_web_sm` (install with
  `python -m spacy download en_core_web_sm`)
- Full pinned versions in `requirements.txt`
- Note: without the spaCy model, scripts run in a reduced mode (surface forms,
  no dependency parse) and some outputs differ. The model must be installed to
  reproduce the reported figures.

## Reproducing the analysis
