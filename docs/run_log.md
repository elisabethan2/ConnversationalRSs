## 2026-06-26 15:27:48 — 02_emergence_curve.py
- git: (not a git repo / git unavailable)
- inputs:
  - ConnversationalRSs/outputs/merged_scopus_wos_2026-06-25.csv
- outputs:
  - ConnversationalRSs/outputs/figures/fig1_emergence_curve_2026-06-26.png
  - ConnversationalRSs/outputs/fig1_emergence_data_2026-06-26.csv
- params: PARTIAL_YEAR=2026
- notes: 866 records; 80% 2020+; peak 2025
- env: python 3.13.12 | pandas 2.3.3 | numpy 2.4.3 | matplotlib 3.10.9

---

## 2026-06-26 15:31:14 — 01_merge_scopus_wos.py
- git: (not a git repo / git unavailable)
- inputs:
  - ConnversationalRSs/data/scopus_export_Jun 25-2026_287a6b90-95ed-44cd-be08-8d6ada4fad16.csv
  - ConnversationalRSs/data/savedrecs (1).txt
  - ConnversationalRSs/data/savedrecs (2).txt
- outputs:
  - ConnversationalRSs/outputs/merged_scopus_wos_2026-06-26.csv
  - ConnversationalRSs/outputs/merge_crossdb_report_2026-06-26.md
- params: dedup: DOI then title+year; primary=Scopus on 'both'
- notes: scopus=783, wos=515 -> union 866 (scopus-only 352, wos-only 93, both 421)
- env: python 3.13.12 | pandas 2.3.3 | numpy 2.4.3 | matplotlib 3.10.9

---

## 2026-06-29 14:49:32 — 04_lexical_analysis.py
- git: (not a git repo / git unavailable)
- inputs:
  - ConnversationalRSs/outputs/merged_scopus_wos_2026-06-26.csv
- outputs:
  - ConnversationalRSs/outputs/colloc_all_nodes_2026-06-29.csv
  - ConnversationalRSs/outputs/register_by_band_2026-06-29.csv
  - ConnversationalRSs/outputs/figures/fig_register_asymmetry_2026-06-29.png
  - ConnversationalRSs/outputs/kwic_2026-06-29.csv
  - ConnversationalRSs/outputs/definitions_2026-06-29.csv
- params: window=±4, min_cooc=3, min_coll_freq=5, bands=['Origins (<=2017)', 'Neural turn (2018-2022)', 'LLM/genAI (2023+)'], nlp=en_core_web_sm 3.8.0
- notes: 866 records; instrumental/interactional overall = 1955/552
- env: python 3.13.12 | pandas 2.3.3 | numpy 2.4.3 | matplotlib 3.10.9 | spacy 3.8.14

---

## 2026-06-29 15:07:34 — 04_lexical_analysis.py
- git: (not a git repo / git unavailable)
- inputs:
  - ConnversationalRSs/outputs/merged_scopus_wos_2026-06-26.csv
- outputs:
  - ConnversationalRSs/outputs/colloc_all_nodes_2026-06-29.csv
  - ConnversationalRSs/outputs/register_by_band_2026-06-29.csv
  - ConnversationalRSs/outputs/register_hits_2026-06-29.csv
  - ConnversationalRSs/outputs/figures/fig_register_asymmetry_2026-06-29.png
  - ConnversationalRSs/outputs/kwic_2026-06-29.csv
  - ConnversationalRSs/outputs/definitions_2026-06-29.csv
- params: window=±4, min_cooc=3, min_coll_freq=5, bands=['Origins (<=2017)', 'Neural turn (2018-2022)', 'LLM/genAI (2023+)'], nlp=en_core_web_sm 3.8.0
- notes: 866 records; instrumental/interactional overall = 1955/552
- env: python 3.13.12 | pandas 2.3.3 | numpy 2.4.3 | matplotlib 3.10.9 | spacy 3.8.14

---

## 2026-06-29 15:52:55 — 04_lexical_analysis.py
- git: (not a git repo / git unavailable)
- inputs:
  - ConnversationalRSs/outputs/merged_scopus_wos_2026-06-26.csv
- outputs:
  - ConnversationalRSs/outputs/colloc_all_nodes_2026-06-29.csv
  - ConnversationalRSs/outputs/register_by_band_2026-06-29.csv
  - ConnversationalRSs/outputs/register_hits_2026-06-29.csv
  - ConnversationalRSs/outputs/interactional_lexicon_audit_2026-06-29.csv
  - ConnversationalRSs/outputs/figures/fig_register_asymmetry_2026-06-29.png
  - ConnversationalRSs/outputs/kwic_2026-06-29.csv
  - ConnversationalRSs/outputs/definitions_2026-06-29.csv
- params: window=±4, min_cooc=3, min_coll_freq=5, bands=['Origins (<=2017)', 'Neural turn (2018-2022)', 'LLM/genAI (2023+)'], nlp=en_core_web_sm 3.8.0
- notes: 866 records; instrumental/interactional overall = 1955/3
- env: python 3.13.12 | pandas 2.3.3 | numpy 2.4.3 | matplotlib 3.10.9 | spacy 3.8.14

---

## 2026-06-29 16:23:43 — 04_lexical_analysis.py
- git: (not a git repo / git unavailable)
- inputs:
  - ConnversationalRSs/outputs/merged_scopus_wos_2026-06-26.csv
- outputs:
  - ConnversationalRSs/outputs/colloc_all_nodes_2026-06-29.csv
  - ConnversationalRSs/outputs/register_by_band_2026-06-29.csv
  - ConnversationalRSs/outputs/register_hits_2026-06-29.csv
  - ConnversationalRSs/outputs/interactional_lexicon_audit_2026-06-29.csv
  - ConnversationalRSs/outputs/figures/fig_register_asymmetry_2026-06-29.png
  - ConnversationalRSs/outputs/kwic_2026-06-29.csv
  - ConnversationalRSs/outputs/definitions_2026-06-29.csv
- params: window=±4, min_cooc=3, min_coll_freq=5, bands=['Origins (<=2017)', 'Neural turn (2018-2022)', 'LLM/genAI (2023+)'], nlp=en_core_web_sm 3.8.0
- notes: 866 records; instrumental/interactional overall = 1955/3
- env: python 3.13.12 | pandas 2.3.3 | numpy 2.4.3 | matplotlib 3.10.9 | spacy 3.8.14

---

## 2026-06-29 16:24:23 — 04_lexical_analysis.py
- git: (not a git repo / git unavailable)
- inputs:
  - ConnversationalRSs/outputs/merged_scopus_wos_2026-06-26.csv
- outputs:
  - ConnversationalRSs/outputs/colloc_all_nodes_2026-06-29.csv
  - ConnversationalRSs/outputs/register_by_band_2026-06-29.csv
  - ConnversationalRSs/outputs/register_hits_2026-06-29.csv
  - ConnversationalRSs/outputs/interactional_lexicon_audit_2026-06-29.csv
  - ConnversationalRSs/outputs/figures/fig_register_asymmetry_2026-06-29.png
  - ConnversationalRSs/outputs/kwic_2026-06-29.csv
  - ConnversationalRSs/outputs/definitions_2026-06-29.csv
- params: window=±4, min_cooc=3, min_coll_freq=5, bands=['Origins (<=2017)', 'Neural turn (2018-2022)', 'LLM/genAI (2023+)'], nlp=en_core_web_sm 3.8.0
- notes: 866 records; instrumental/interactional overall = 1955/3
- env: python 3.13.12 | pandas 2.3.3 | numpy 2.4.3 | matplotlib 3.10.9 | networkx 3.6.1 | spacy 3.8.14

---

## 2026-06-29 16:40:04 — 04_lexical_analysis.py
- git: (not a git repo / git unavailable)
- inputs:
  - ConnversationalRSs/outputs/merged_scopus_wos_2026-06-26.csv
- outputs:
  - ConnversationalRSs/outputs/colloc_all_nodes_2026-06-29.csv
  - ConnversationalRSs/outputs/register_by_band_2026-06-29.csv
  - ConnversationalRSs/outputs/register_hits_2026-06-29.csv
  - ConnversationalRSs/outputs/interactional_lexicon_audit_2026-06-29.csv
  - ConnversationalRSs/outputs/figures/fig_register_asymmetry_2026-06-29.png
  - ConnversationalRSs/outputs/kwic_2026-06-29.csv
  - ConnversationalRSs/outputs/definitions_2026-06-29.csv
- params: window=±4, min_cooc=3, min_coll_freq=5, bands=['Origins (<=2017)', 'Neural turn (2018-2022)', 'LLM/genAI (2023+)'], nlp=en_core_web_sm 3.8.0
- notes: 866 records; instrumental/interactional overall = 1955/3
- env: python 3.13.12 | pandas 2.3.3 | numpy 2.4.3 | matplotlib 3.10.9 | networkx 3.6.1 | spacy 3.8.14

---

## 2026-06-30 08:41:02 — 03_corpus_profile.py
- git: (not a git repo / git unavailable)
- inputs:
  - ConnversationalRSs/outputs/merged_scopus_wos_2026-06-26.csv
- outputs:
  - ConnversationalRSs/outputs/figures/fig_corpus_profile_2026-06-30.png
  - ConnversationalRSs/outputs/corpus_profile_doctypes_2026-06-30.csv
  - ConnversationalRSs/outputs/corpus_profile_venues_2026-06-30.csv
  - ConnversationalRSs/outputs/corpus_profile_language_2026-06-30.csv
- notes: 866 records; English 859; conference 670, article 169
- env: python 3.13.12 | pandas 2.3.3 | numpy 2.4.3 | matplotlib 3.10.9

---

## 2026-06-30 08:41:53 — make_cluster_worksheet.py
- git: (not a git repo / git unavailable)
- inputs:
  - ConnversationalRSs/outputs/VOSViewerOutputFiles/mapMin5AuthorOccurencesRes0_6_250626.txt
- outputs:
  - ConnversationalRSs/outputs/cluster_naming_worksheet_2026-06-30.md
- params: min-5 / res-0.6 primary map
- notes: 8 clusters, 58 terms
- env: python 3.13.12 | pandas 2.3.3 | numpy 2.4.3 | matplotlib 3.10.9

---

## 2026-06-30 09:34:34 — 04_lexical_analysis.py
- git: (not a git repo / git unavailable)
- inputs:
  - ConnversationalRSs/outputs/merged_scopus_wos_2026-06-26.csv
- outputs:
  - ConnversationalRSs/outputs/colloc_all_nodes_2026-06-30.csv
  - ConnversationalRSs/outputs/register_by_band_2026-06-30.csv
  - ConnversationalRSs/outputs/register_hits_2026-06-30.csv
  - ConnversationalRSs/outputs/interactional_lexicon_audit_2026-06-30.csv
  - ConnversationalRSs/outputs/figures/fig_register_asymmetry_2026-06-30.png
  - ConnversationalRSs/outputs/kwic_2026-06-30.csv
  - ConnversationalRSs/outputs/definitions_2026-06-30.csv
- params: window=±4, min_cooc=3, min_coll_freq=5, bands=['Origins (<=2017)', 'Neural turn (2018-2022)', 'LLM/genAI (2023+)'], nlp=en_core_web_sm 3.8.0
- notes: 866 records; instrumental/interactional overall = 1955/4
- env: python 3.13.12 | pandas 2.3.3 | numpy 2.4.3 | matplotlib 3.10.9 | spacy 3.8.14

---

## 2026-06-30 09:36:28 — 04_lexical_analysis.py
- git: (not a git repo / git unavailable)
- inputs:
  - ConnversationalRSs/outputs/merged_scopus_wos_2026-06-26.csv
- outputs:
  - ConnversationalRSs/outputs/colloc_all_nodes_2026-06-30.csv
  - ConnversationalRSs/outputs/register_by_band_2026-06-30.csv
  - ConnversationalRSs/outputs/register_hits_2026-06-30.csv
  - ConnversationalRSs/outputs/interactional_lexicon_audit_2026-06-30.csv
  - ConnversationalRSs/outputs/figures/fig_register_asymmetry_2026-06-30.png
  - ConnversationalRSs/outputs/kwic_2026-06-30.csv
  - ConnversationalRSs/outputs/definitions_2026-06-30.csv
- params: window=±4, min_cooc=3, min_coll_freq=5, bands=['Origins (<=2017)', 'Neural turn (2018-2022)', 'LLM/genAI (2023+)'], nlp=en_core_web_sm 3.8.0
- notes: 866 records; instrumental/interactional overall = 1955/4
- env: python 3.13.12 | pandas 2.3.3 | numpy 2.4.3 | matplotlib 3.10.9 | spacy 3.8.14

---

## 2026-06-30 10:07:53 — 04_lexical_analysis.py
- git: (not a git repo / git unavailable)
- inputs:
  - ConnversationalRSs/outputs/merged_scopus_wos_2026-06-26.csv
- outputs:
  - ConnversationalRSs/outputs/colloc_all_nodes_2026-06-30.csv
  - ConnversationalRSs/outputs/register_by_band_2026-06-30.csv
  - ConnversationalRSs/outputs/register_hits_2026-06-30.csv
  - ConnversationalRSs/outputs/interactional_lexicon_audit_2026-06-30.csv
  - ConnversationalRSs/outputs/figures/fig_register_asymmetry_2026-06-30.png
  - ConnversationalRSs/outputs/kwic_2026-06-30.csv
  - ConnversationalRSs/outputs/definitions_2026-06-30.csv
- params: window=±4, min_cooc=3, min_coll_freq=5, bands=['Origins (<=2017)', 'Neural turn (2018-2022)', 'LLM/genAI (2023+)'], nlp=en_core_web_sm 3.8.0
- notes: 866 records; instrumental/interactional overall = 1955/4
- env: python 3.13.12 | pandas 2.3.3 | numpy 2.4.3 | matplotlib 3.10.9 | networkx 3.6.1 | spacy 3.8.14

---

## 2026-06-30 10:16:39 — 04_lexical_analysis.py
- git: (not a git repo / git unavailable)
- inputs:
  - ConnversationalRSs/outputs/merged_scopus_wos_2026-06-26.csv
- outputs:
  - ConnversationalRSs/outputs/colloc_all_nodes_2026-06-30.csv
  - ConnversationalRSs/outputs/register_by_band_2026-06-30.csv
  - ConnversationalRSs/outputs/register_hits_2026-06-30.csv
  - ConnversationalRSs/outputs/interactional_lexicon_audit_2026-06-30.csv
  - ConnversationalRSs/outputs/figures/fig_register_asymmetry_2026-06-30.png
  - ConnversationalRSs/outputs/kwic_2026-06-30.csv
  - ConnversationalRSs/outputs/definitions_2026-06-30.csv
- params: window=±4, min_cooc=3, min_coll_freq=5, bands=['Origins (<=2017)', 'Neural turn (2018-2022)', 'LLM/genAI (2023+)'], nlp=en_core_web_sm 3.8.0
- notes: 866 records; instrumental/interactional overall = 1955/4
- env: python 3.13.12 | pandas 2.3.3 | numpy 2.4.3 | matplotlib 3.10.9 | networkx 3.6.1 | spacy 3.8.14

---

## 2026-06-30 10:21:43 — 04_lexical_analysis.py
- git: (not a git repo / git unavailable)
- inputs:
  - ConnversationalRSs/outputs/merged_scopus_wos_2026-06-26.csv
- outputs:
  - ConnversationalRSs/outputs/colloc_all_nodes_2026-06-30.csv
  - ConnversationalRSs/outputs/register_by_band_2026-06-30.csv
  - ConnversationalRSs/outputs/register_hits_2026-06-30.csv
  - ConnversationalRSs/outputs/interactional_lexicon_audit_2026-06-30.csv
  - ConnversationalRSs/outputs/figures/fig_register_asymmetry_2026-06-30.png
  - ConnversationalRSs/outputs/kwic_2026-06-30.csv
  - ConnversationalRSs/outputs/definitions_2026-06-30.csv
- params: window=±4, min_cooc=3, min_coll_freq=5, bands=['Origins (<=2017)', 'Neural turn (2018-2022)', 'LLM/genAI (2023+)'], nlp=en_core_web_sm 3.8.0
- notes: 866 records; instrumental/interactional overall = 1955/4
- env: python 3.13.12 | pandas 2.3.3 | numpy 2.4.3 | matplotlib 3.10.9 | networkx 3.6.1 | spacy 3.8.14

---

## 2026-06-30 10:25:37 — 04_lexical_analysis.py
- git: (not a git repo / git unavailable)
- inputs:
  - ConnversationalRSs/outputs/merged_scopus_wos_2026-06-26.csv
- outputs:
  - ConnversationalRSs/outputs/colloc_all_nodes_2026-06-30.csv
  - ConnversationalRSs/outputs/register_by_band_2026-06-30.csv
  - ConnversationalRSs/outputs/register_hits_2026-06-30.csv
  - ConnversationalRSs/outputs/interactional_lexicon_audit_2026-06-30.csv
  - ConnversationalRSs/outputs/figures/fig_register_asymmetry_2026-06-30.png
  - ConnversationalRSs/outputs/kwic_2026-06-30.csv
  - ConnversationalRSs/outputs/definitions_2026-06-30.csv
- params: window=±4, min_cooc=3, min_coll_freq=5, bands=['Origins (<=2017)', 'Neural turn (2018-2022)', 'LLM/genAI (2023+)'], nlp=en_core_web_sm 3.8.0
- notes: 866 records; instrumental/interactional overall = 1955/4
- env: python 3.13.12 | pandas 2.3.3 | numpy 2.4.3 | matplotlib 3.10.9 | networkx 3.6.1 | spacy 3.8.14

---

## 2026-06-30 10:43:41 — 04_lexical_analysis.py
- git: (not a git repo / git unavailable)
- inputs:
  - ConnversationalRSs/outputs/merged_scopus_wos_2026-06-26.csv
- outputs:
  - ConnversationalRSs/outputs/colloc_all_nodes_2026-06-30.csv
  - ConnversationalRSs/outputs/register_by_band_2026-06-30.csv
  - ConnversationalRSs/outputs/register_hits_2026-06-30.csv
  - ConnversationalRSs/outputs/interactional_lexicon_audit_2026-06-30.csv
  - ConnversationalRSs/outputs/figures/fig_register_asymmetry_2026-06-30.png
  - ConnversationalRSs/outputs/kwic_2026-06-30.csv
  - ConnversationalRSs/outputs/definitions_2026-06-30.csv
- params: window=±4, min_cooc=3, min_coll_freq=5, bands=['Origins (<=2017)', 'Neural turn (2018-2022)', 'LLM/genAI (2023+)'], nlp=en_core_web_sm 3.8.0
- notes: 866 records; instrumental/interactional overall = 1955/4
- env: python 3.13.12 | pandas 2.3.3 | numpy 2.4.3 | matplotlib 3.10.9 | networkx 3.6.1 | spacy 3.8.14

---

## 2026-07-13 10:01:30 — 06_appendix_lexicon.py
- git: (not a git repo / git unavailable)
- inputs:
  - ConnversationalRSs/outputs/interactional_lexicon_audit_2026-06-30.csv
- outputs:
  - ConnversationalRSs/outputs/appendix_interactional_lexicon_2026-07-13.csv
  - ConnversationalRSs/outputs/appendix_interactional_lexicon_2026-07-13.md
- params: deterministic; no randomness; formats audit CSV only
- notes: python-docx=absent; layers=['CA_core', 'pragmatics', 'hci_cui']
- env: python 3.13.12 | pandas 2.3.3 | numpy 2.4.3 | matplotlib 3.10.9

---

## 2026-07-13 10:05:50 — 06_appendix_lexicon.py
- git: (not a git repo / git unavailable)
- inputs:
  - ConnversationalRSs/outputs/interactional_lexicon_audit_2026-06-30.csv
- outputs:
  - ConnversationalRSs/outputs/appendix_interactional_lexicon_2026-07-13.csv
  - ConnversationalRSs/outputs/appendix_interactional_lexicon_2026-07-13.md
  - ConnversationalRSs/outputs/appendix_interactional_lexicon_2026-07-13.docx
- params: deterministic; no randomness; formats audit CSV only
- notes: python-docx=1.2.0; layers=['CA_core', 'pragmatics', 'hci_cui']
- env: python 3.13.12 | pandas 2.3.3 | numpy 2.4.3 | matplotlib 3.10.9

---

## 2026-07-13 10:23:07 — 04_lexical_analysisV2.py
- git: (not a git repo / git unavailable)
- inputs:
  - ConnversationalRSs/outputs/merged_scopus_wos_2026-06-26.csv
- outputs:
  - ConnversationalRSs/outputs/colloc_all_nodes_2026-07-13.csv
  - ConnversationalRSs/outputs/register_by_band_2026-07-13.csv
  - ConnversationalRSs/outputs/register_hits_2026-07-13.csv
  - ConnversationalRSs/outputs/interactional_lexicon_audit_2026-07-13.csv
  - ConnversationalRSs/outputs/interactional_layer_union_2026-07-13.csv
  - ConnversationalRSs/outputs/figures/fig_register_asymmetry_2026-07-13.png
  - ConnversationalRSs/outputs/kwic_2026-07-13.csv
  - ConnversationalRSs/outputs/definitions_2026-07-13.csv
- params: window=±4, min_cooc=3, min_coll_freq=5, bands=['Origins (<=2017)', 'Neural turn (2018-2022)', 'LLM/genAI (2023+)'], nlp=spacy.blank('en') (NO MODEL: surface forms, no POS)
- notes: 866 records; instrumental/interactional overall = 1468/4
- env: python 3.13.12 | pandas 2.3.3 | numpy 2.4.3 | matplotlib 3.10.9 | spacy 3.8.14

---

## 2026-07-13 10:23:14 — 07_section6_collocation_profile.py
- git: (not a git repo / git unavailable)
- inputs:
  - ConnversationalRSs/outputs/register_hits_2026-07-13.csv
- outputs:
  - ConnversationalRSs/outputs/colloc_profile_2026-07-13.csv
  - ConnversationalRSs/outputs/figures/fig_colloc_profile_2026-07-13.png
- params: register=instrumental, metric=records, top=15, collapse=none
- notes: base_records=527; deterministic (no randomness)
- env: python 3.13.12 | pandas 2.3.3 | numpy 2.4.3 | matplotlib 3.10.9 | spacy 3.8.14

---

## 2026-07-13 10:24:22 — 04_lexical_analysisV2.py
- git: (not a git repo / git unavailable)
- inputs:
  - ConnversationalRSs/outputs/merged_scopus_wos_2026-06-26.csv
- outputs:
  - ConnversationalRSs/outputs/colloc_all_nodes_2026-07-13.csv
  - ConnversationalRSs/outputs/register_by_band_2026-07-13.csv
  - ConnversationalRSs/outputs/register_hits_2026-07-13.csv
  - ConnversationalRSs/outputs/interactional_lexicon_audit_2026-07-13.csv
  - ConnversationalRSs/outputs/interactional_layer_union_2026-07-13.csv
  - ConnversationalRSs/outputs/figures/fig_register_asymmetry_2026-07-13.png
  - ConnversationalRSs/outputs/kwic_2026-07-13.csv
  - ConnversationalRSs/outputs/definitions_2026-07-13.csv
- params: window=±4, min_cooc=3, min_coll_freq=5, bands=['Origins (<=2017)', 'Neural turn (2018-2022)', 'LLM/genAI (2023+)'], nlp=spacy.blank('en') (NO MODEL: surface forms, no POS)
- notes: 866 records; instrumental/interactional overall = 1468/4
- env: python 3.13.12 | pandas 2.3.3 | numpy 2.4.3 | matplotlib 3.10.9 | networkx 3.6.1 | spacy 3.8.14

---

## 2026-07-13 10:25:34 — 04_lexical_analysisV2.py
- git: (not a git repo / git unavailable)
- inputs:
  - ConnversationalRSs/outputs/merged_scopus_wos_2026-06-26.csv
- outputs:
  - ConnversationalRSs/outputs/colloc_all_nodes_2026-07-13.csv
  - ConnversationalRSs/outputs/register_by_band_2026-07-13.csv
  - ConnversationalRSs/outputs/register_hits_2026-07-13.csv
  - ConnversationalRSs/outputs/interactional_lexicon_audit_2026-07-13.csv
  - ConnversationalRSs/outputs/interactional_layer_union_2026-07-13.csv
  - ConnversationalRSs/outputs/figures/fig_register_asymmetry_2026-07-13.png
  - ConnversationalRSs/outputs/kwic_2026-07-13.csv
  - ConnversationalRSs/outputs/definitions_2026-07-13.csv
- params: window=±4, min_cooc=3, min_coll_freq=5, bands=['Origins (<=2017)', 'Neural turn (2018-2022)', 'LLM/genAI (2023+)'], nlp=en_core_web_sm 3.8.0
- notes: 866 records; instrumental/interactional overall = 1955/4
- env: python 3.13.12 | pandas 2.3.3 | numpy 2.4.3 | matplotlib 3.10.9 | networkx 3.6.1 | spacy 3.8.14

---

## 2026-07-13 10:35:30 — 04_lexical_analysisV2.py
- git: (not a git repo / git unavailable)
- inputs:
  - ConnversationalRSs/outputs/merged_scopus_wos_2026-06-26.csv
- outputs:
  - ConnversationalRSs/outputs/colloc_all_nodes_2026-07-13.csv
  - ConnversationalRSs/outputs/register_by_band_2026-07-13.csv
  - ConnversationalRSs/outputs/register_hits_2026-07-13.csv
  - ConnversationalRSs/outputs/interactional_lexicon_audit_2026-07-13.csv
  - ConnversationalRSs/outputs/interactional_layer_union_2026-07-13.csv
  - ConnversationalRSs/outputs/figures/fig_register_asymmetry_2026-07-13.png
  - ConnversationalRSs/outputs/kwic_2026-07-13.csv
  - ConnversationalRSs/outputs/definitions_2026-07-13.csv
- params: window=±4, min_cooc=3, min_coll_freq=5, bands=['Origins (<=2017)', 'Neural turn (2018-2022)', 'LLM/genAI (2023+)'], nlp=en_core_web_sm 3.8.0
- notes: 866 records; instrumental/interactional overall = 1955/4
- env: python 3.13.12 | pandas 2.3.3 | numpy 2.4.3 | matplotlib 3.10.9 | networkx 3.6.1 | spacy 3.8.14

---

## 2026-07-13 10:37:32 — 04_lexical_analysisV2.py
- git: (not a git repo / git unavailable)
- inputs:
  - ConnversationalRSs/outputs/merged_scopus_wos_2026-06-26.csv
- outputs:
  - ConnversationalRSs/outputs/colloc_all_nodes_2026-07-13.csv
  - ConnversationalRSs/outputs/register_by_band_2026-07-13.csv
  - ConnversationalRSs/outputs/register_hits_2026-07-13.csv
  - ConnversationalRSs/outputs/interactional_lexicon_audit_2026-07-13.csv
  - ConnversationalRSs/outputs/interactional_layer_union_2026-07-13.csv
  - ConnversationalRSs/outputs/figures/fig_register_asymmetry_2026-07-13.png
  - ConnversationalRSs/outputs/kwic_2026-07-13.csv
  - ConnversationalRSs/outputs/definitions_2026-07-13.csv
- params: window=±4, min_cooc=3, min_coll_freq=5, bands=['Origins (<=2017)', 'Neural turn (2018-2022)', 'LLM/genAI (2023+)'], nlp=en_core_web_sm 3.8.0
- notes: 866 records; instrumental/interactional overall = 1955/4
- env: python 3.13.12 | pandas 2.3.3 | numpy 2.4.3 | matplotlib 3.10.9 | networkx 3.6.1 | spacy 3.8.14

---

## 2026-07-13 10:43:05 — 07_section6_collocation_profile.py
- git: (not a git repo / git unavailable)
- inputs:
  - ConnversationalRSs/outputs/register_hits_2026-07-13.csv
- outputs:
  - ConnversationalRSs/outputs/colloc_profile_2026-07-13.csv
  - ConnversationalRSs/outputs/figures/fig_colloc_profile_2026-07-13.png
- params: register=instrumental, metric=records, top=15, collapse=none
- notes: base_records=584; deterministic (no randomness)
- env: python 3.13.12 | pandas 2.3.3 | numpy 2.4.3 | matplotlib 3.10.9 | networkx 3.6.1 | spacy 3.8.14

---

## 2026-07-13 10:47:46 — 07_section6_collocation_profile.py
- git: (not a git repo / git unavailable)
- inputs:
  - ConnversationalRSs/outputs/register_hits_2026-07-13.csv
- outputs:
  - ConnversationalRSs/outputs/colloc_profile_2026-07-13.csv
  - ConnversationalRSs/outputs/figures/fig_colloc_profile_2026-07-13.png
- params: register=instrumental, metric=records, top=15, collapse={'modeling': 'model', 'learn': 'learning'}
- notes: base_records=584; deterministic (no randomness)
- env: python 3.13.12 | pandas 2.3.3 | numpy 2.4.3 | matplotlib 3.10.9 | networkx 3.6.1 | spacy 3.8.14

---
## 2026-07-13 11.24.00
spaCy functional in-session; the 2026-07-13 04 run executed in reduced mode (model-dependent outputs identical to pre-model run); Section 6 relies only on model-independent outputs (register test, gradient, profile), so results stand; methods wording corrected to drop the lemmatisation claim.## 2026-07-13 13:42:04 — 07_section6_collocation_profile.py
- git: (not a git repo / git unavailable)
- inputs:
  - ConnversationalRSs/outputs/register_hits_2026-07-13.csv
- outputs:
  - ConnversationalRSs/outputs/colloc_profile_2026-07-13.csv
  - ConnversationalRSs/outputs/figures/fig_colloc_profile_2026-07-13.png
- params: register=instrumental, metric=records, top=15, collapse={'modeling': 'model', 'learn': 'learning', 'eliciting': 'elicit'}
- notes: base_records=584; deterministic (no randomness)
- env: python 3.13.12 | pandas 2.3.3 | numpy 2.4.3 | matplotlib 3.10.9 | networkx 3.6.1 | spacy 3.8.14

---

## 2026-07-13 13:43:30 — 07_section6_collocation_profile.py
- git: (not a git repo / git unavailable)
- inputs:
  - ConnversationalRSs/outputs/register_hits_2026-07-13.csv
- outputs:
  - ConnversationalRSs/outputs/colloc_profile_2026-07-13.csv
  - ConnversationalRSs/outputs/figures/fig_colloc_profile_2026-07-13.png
- params: register=instrumental, metric=records, top=15, collapse={'modeling': 'model', 'learn': 'learning', 'elicitation': 'elicit'}
- notes: base_records=584; deterministic (no randomness)
- env: python 3.13.12 | pandas 2.3.3 | numpy 2.4.3 | matplotlib 3.10.9 | networkx 3.6.1 | spacy 3.8.14

---

## 2026-07-13 14:06:14 — 04_lexical_analysis.py
- git: (not a git repo / git unavailable)
- inputs:
  - ConnversationalRSs/outputs/merged_scopus_wos_2026-06-26.csv
- outputs:
  - ConnversationalRSs/outputs/colloc_all_nodes_2026-07-13.csv
  - ConnversationalRSs/outputs/register_by_band_2026-07-13.csv
  - ConnversationalRSs/outputs/register_hits_2026-07-13.csv
  - ConnversationalRSs/outputs/interactional_lexicon_audit_2026-07-13.csv
  - ConnversationalRSs/outputs/figures/fig_register_asymmetry_2026-07-13.png
  - ConnversationalRSs/outputs/kwic_2026-07-13.csv
  - ConnversationalRSs/outputs/definitions_2026-07-13.csv
- params: window=±4, min_cooc=3, min_coll_freq=5, bands=['Origins (<=2017)', 'Neural turn (2018-2022)', 'LLM/genAI (2023+)'], nlp=en_core_web_sm 3.8.0
- notes: 866 records; instrumental/interactional overall = 1955/4
- env: python 3.13.12 | pandas 2.3.3 | numpy 2.4.3 | matplotlib 3.10.9 | networkx 3.6.1 | spacy 3.8.14

---

## 2026-07-13 14:11:37 — 04_lexical_analysis.py
- git: (not a git repo / git unavailable)
- inputs:
  - ConnversationalRSs/outputs/merged_scopus_wos_2026-06-26.csv
- outputs:
  - ConnversationalRSs/outputs/colloc_all_nodes_2026-07-13.csv
  - ConnversationalRSs/outputs/register_by_band_2026-07-13.csv
  - ConnversationalRSs/outputs/register_hits_2026-07-13.csv
  - ConnversationalRSs/outputs/interactional_lexicon_audit_2026-07-13.csv
  - ConnversationalRSs/outputs/figures/fig_register_asymmetry_2026-07-13.png
  - ConnversationalRSs/outputs/kwic_2026-07-13.csv
  - ConnversationalRSs/outputs/definitions_2026-07-13.csv
- params: window=±4, min_cooc=3, min_coll_freq=5, bands=['Origins (<=2017)', 'Neural turn (2018-2022)', 'LLM/genAI (2023+)'], nlp=en_core_web_sm 3.8.0
- notes: 866 records; instrumental/interactional overall = 1955/4
- env: python 3.13.12 | pandas 2.3.3 | numpy 2.4.3 | matplotlib 3.10.9 | networkx 3.6.1 | spacy 3.8.14

---

## 2026-07-13 14:12:15 — 04_lexical_analysisV2.py
- git: (not a git repo / git unavailable)
- inputs:
  - ConnversationalRSs/outputs/merged_scopus_wos_2026-06-26.csv
- outputs:
  - ConnversationalRSs/outputs/colloc_all_nodes_2026-07-13.csv
  - ConnversationalRSs/outputs/register_by_band_2026-07-13.csv
  - ConnversationalRSs/outputs/register_hits_2026-07-13.csv
  - ConnversationalRSs/outputs/interactional_lexicon_audit_2026-07-13.csv
  - ConnversationalRSs/outputs/interactional_layer_union_2026-07-13.csv
  - ConnversationalRSs/outputs/figures/fig_register_asymmetry_2026-07-13.png
  - ConnversationalRSs/outputs/kwic_2026-07-13.csv
  - ConnversationalRSs/outputs/definitions_2026-07-13.csv
- params: window=±4, min_cooc=3, min_coll_freq=5, bands=['Origins (<=2017)', 'Neural turn (2018-2022)', 'LLM/genAI (2023+)'], nlp=en_core_web_sm 3.8.0
- notes: 866 records; instrumental/interactional overall = 1955/4
- env: python 3.13.12 | pandas 2.3.3 | numpy 2.4.3 | matplotlib 3.10.9 | networkx 3.6.1 | spacy 3.8.14

---

## 2026-07-13 14:12:51 — 06_appendix_lexicon.py
- git: (not a git repo / git unavailable)
- inputs:
  - ConnversationalRSs/outputs/interactional_lexicon_audit_2026-07-13.csv
- outputs:
  - ConnversationalRSs/outputs/appendix_interactional_lexicon_2026-07-13.csv
  - ConnversationalRSs/outputs/appendix_interactional_lexicon_2026-07-13.md
  - ConnversationalRSs/outputs/appendix_interactional_lexicon_2026-07-13.docx
- params: deterministic; no randomness; formats audit CSV only
- notes: python-docx=1.2.0; layers=['CA_core', 'pragmatics', 'hci_cui']
- env: python 3.13.12 | pandas 2.3.3 | numpy 2.4.3 | matplotlib 3.10.9 | networkx 3.6.1 | spacy 3.8.14

---

## 2026-07-13 14:16:19 — 07_section6_collocation_profile.py
- git: (not a git repo / git unavailable)
- inputs:
  - ConnversationalRSs/outputs/register_hits_2026-07-13.csv
- outputs:
  - ConnversationalRSs/outputs/colloc_profile_2026-07-13.csv
  - ConnversationalRSs/outputs/figures/fig_colloc_profile_2026-07-13.png
- params: register=instrumental, metric=records, top=15, collapse={'modeling': 'model', 'learn': 'learning', 'elicitation': 'elicit'}
- notes: base_records=584; deterministic (no randomness)
- env: python 3.13.12 | pandas 2.3.3 | numpy 2.4.3 | matplotlib 3.10.9 | networkx 3.6.1 | spacy 3.8.14

---

