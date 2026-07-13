# Cross-database merge report -- 2026-06-25

Generated: 2026-06-25T21:39:51

## Inputs (raw, immutable)
- Scopus: 783 records (matched `scopus_export*.csv`)
- Web of Science: 515 records after within-WoS de-duplication on UT
  (matched `savedrecs*.txt`, concatenated across files)

## Output
- Union corpus: `merged_scopus_wos_2026-06-25.csv`  (866 unique records, Scopus column layout)

## De-duplication
Key = normalized DOI if present, else normalized (title + year).
Title normalization: lowercase, non-alphanumeric -> space, whitespace collapsed.
On a record present in both databases the **Scopus** copy is kept as primary.

| provenance (source_db) | records |
|------------------------|--------:|
| scopus only | 352 |
| wos only    | 93 |
| both        | 421 |
| **total unique** | **866** |

Keys resolved by: {'doi': 658, 'title_year': 208}

**Overlap reading:** 421 records appear in both databases; WoS adds
93 records not in Scopus. (Scopus contributed 783; WoS
contributed 515; union 866.)

## WoS -> Scopus field mapping
| WoS tag | Scopus column |
|---------|---------------|
| AU | Authors |
| AF | Author full names |
| TI | Title |
| PY | Year |
| SO | Source title |
| VL | Volume |
| IS | Issue |
| AR | Art. No. |
| BP | Page start |
| EP | Page end |
| TC | Cited by |
| DI | DOI |
| AB | Abstract |
| DE | Author Keywords |
| ID | Index Keywords |
| CR | References |
| PU | Publisher |
| SN | ISSN |
| BN | ISBN |
| PM | PubMed ID |
| LA | Language of Original Document |
| J9 | Abbreviated Source Title |
| DT | Document Type |
| CT | Conference name |
| CY | Conference date |
| CL | Conference location |
WoS `WC` (categories) and `SC` (research areas) are carried as extra columns
(no Scopus-CSV equivalent); `UT` is carried as `wos_UT`.

## Reference / citation caveat
References are carried in each record's native format (`ref_format` = scopus|wos).
Because the two databases format reference strings differently, this union file
is suitable for keyword co-occurrence and descriptive mapping but NOT for
cross-database co-citation or bibliographic coupling. Run those PER DATABASE.

## Environment
- python: 3.13.12
- pandas: 2.3.3
