#!/usr/bin/env python3
"""
04_lexical_analysis.py
======================
Lexical layer for the term-mapping paper: tests the "instrumental" reading of
"conversation" in the CRS corpus and builds material for close reading.

Runs on title + abstract of all records (kept whole; the 7 non-English records
are retained and noted). Produces:

  COLLOCATION
    - colloc_<node>_<date>.csv          ranked collocates per node word (logDice)
    - colloc_all_nodes_<date>.csv        combined
    - fig_colloc_network_conversational_<date>.png   collocation network

  REGISTER TEST (the hypothesis)
    - register_by_band_<date>.csv        instrumental vs interactional collocate
                                         mass, overall and per diachronic band
    - fig_register_asymmetry_<date>.png  grouped bars (the argument-in-a-chart)

  CONCORDANCE / READING MATERIAL
    - kwic_<date>.csv                    keyword-in-context lines for node words
    - definitions_<date>.csv             sentences that appear to *define* terms
    - modifiers_conversational_<date>.csv   what "conversational" modifies
    - modifiers_of_node_nouns_<date>.csv    what modifies conversation/dialogue/…

Diachronic bands (configurable) align with Section 5:
  Origins (<=2017) · Neural turn (2018-2022) · LLM/genAI (2023+).
NB the Origins band is small (~150 records); treat its rare collocates cautiously.

Requires spaCy. For full results install the model on UCloud:
    python -m spacy download en_core_web_sm
If the model is absent the script still runs in a reduced mode (surface forms,
no POS) and says so, so output is comparable but lemmatisation is skipped.

Deterministic: network layout uses a fixed seed; no other randomness.
"""
from __future__ import annotations
import sys, re, math
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path
import pandas as pd

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).resolve().parent))
from runlog import log_run

# ----------------------------------------------------------------------------
# CONFIG
# ----------------------------------------------------------------------------
BASE_DIR = Path("ConnversationalRSs")
OUT_DIR  = BASE_DIR / "outputs"
FIG_DIR  = OUT_DIR / "figures"
MERGED_FILE = None                 # None -> newest merged_scopus_wos_*.csv
RUN_DATE = date.today().isoformat()
SEED = 42

WINDOW = 4                         # collocation window, +/- tokens (content stream)
MIN_COOC = 3                       # min co-occurrences to keep a collocate
MIN_COLL_FREQ = 5                  # min corpus frequency of a collocate
TOP_NETWORK = 20                   # collocates shown in the network figure

# node words (matched on lemma OR surface, so robust with/without the model)
NODE_LEMMAS = {"conversation", "conversational", "dialogue", "dialog",
               "interaction", "interactive", "chat", "utterance",
               "turn", "multi-turn"}
# nodes to concordance / draw (exclude bare 'turn' from KWIC: too noisy)
KWIC_PATTERN = re.compile(
    r"\b(conversation\w*|dialog\w*|interaction\w*|interactive|chat\w*|"
    r"utterance\w*|multi-turn|turn-taking)\b", re.I)
KWIC_CONTEXT = 60                  # characters of context each side

# diachronic bands: (label, low_year_inclusive, high_year_inclusive)
BANDS = [("Origins (<=2017)", -9999, 2017),
         ("Neural turn (2018-2022)", 2018, 2022),
         ("LLM/genAI (2023+)", 2023, 9999)]

# --- registers operationalising the instrumental thesis --------------------
# INSTRUMENTAL + INTERACTIONAL_TOKENS are SINGLE, low-ambiguity tokens used for
# the window collocation/register measure. Overloaded words (context, response,
# turn, sequence, understanding, alignment, ...) are deliberately EXCLUDED here
# because their dominant sense in this corpus is not reliably interactional;
# inspect them with `--inspect <term>` and decide at the type level.
INSTRUMENTAL = {
    "elicit", "elicitation", "elicited", "preference", "preferences",
    "input", "signal", "feedback", "query", "queries", "intent", "data",
    "model", "modeling", "modelling", "learn", "learning", "reward",
    "policy", "optimize", "optimise", "optimization", "slot", "attribute",
    "attributes", "simulate", "simulation", "simulator", "predict",
    "prediction", "profile", "rating", "ratings", "embedding", "embeddings",
    "representation", "vector", "feature", "features", "extract", "capture",
}
# curated, low-ambiguity interactional single tokens (for the window measure)
INTERACTIONAL_TOKENS = {
    "turn-taking", "intersubjectivity", "recipiency", "politeness",
    "impoliteness", "facework", "footing", "anthropomorphism", "rapport",
    "miscommunication",
}

# --- layered interactional lexicon (for the presence / absence audit) -------
# Three DISJOINT layers, each sourced from a standard reference work, reported
# as a "gradient of absence" (interaction-as-object -> meaning -> interface):
#   CA_core      Sidnell & Stivers (2012), The Handbook of Conversation Analysis
#   pragmatics   Verschueren & Östman (2022), Handbook of Pragmatics: Manual
#   hci_cui      Namvarpour & Razi (2025), CUI '25; Wagner et al. (2025), Appl.Sci.
# Shared terms (turn-taking, repair, clarification, progressivity, coherence are
# used by BOTH CA and CUI) are assigned to CA_core only, so the CUI layer holds
# CUI-specific vocabulary. Phrases are matched on raw text. Lexical PRESENCE is
# not conceptual TREATMENT: a CA-core hit is a close-reading candidate, since a
# term (e.g. "turn-taking", "repair") may be used in the engineering sense.
INTERACTIONAL_LEXICON = {
    # interaction-as-object (Sidnell & Stivers 2012)
    "CA_core": {
        "turn-taking", "turn-constructional unit", "turn construction",
        "turn design", "turn allocation", "next-speaker selection",
        "adjacency pair", "adjacency pairs", "first-pair part", "second-pair part",
        "first pair part", "second pair part",
        "sequence organization", "sequence organisation", "sequential organization",
        "sequence expansion", "pre-expansion", "insert expansion", "post-expansion",
        "pre-sequence", "repair", "self-repair", "other-repair",
        "self-initiated repair", "other-initiated repair", "repair initiation",
        "trouble source", "third-position repair", "transition-space repair",
        "transition-relevance place", "recipient design", "recipiency",
        "preference organization", "preference organisation", "dispreferred",
        "social action", "action formation", "membership categorization",
        "membership categorisation", "intersubjectivity", "overall structural organization",
        "progressivity", "projectability", "nextness", "overlap", "coherence",
        "next turn", "third position",
    },
    # meaning-in-interaction (Verschueren & Östman 2022)
    "pragmatics": {
        "politeness", "impoliteness", "face", "face-work", "facework", "footing",
        "speech act", "speech acts", "illocutionary force", "felicity condition",
        "conversational implicature", "implicature", "common ground",
        "mutual knowledge", "deixis", "indexicality", "accommodation",
        "listener response", "backchannel", "terms of address", "silence",
        "participation framework", "stance",
    },
    # interaction-as-interface (Namvarpour & Razi 2025; Wagner et al. 2025)
    "hci_cui": {
        "naturalness", "rapport", "anthropomorphism", "empathy",
        "miscommunication", "breakdown", "conversational breakdown",
        "error recovery", "error handling", "repair strategies",
        "conversational style", "dialogue state tracking", "mixed-initiative",
        "mixed initiative", "multi-party", "multi-user", "attentive listening",
        "engagement", "trust",
    },
}
# terms whose presence in a CS corpus is an unreliable signal (flag, don't trust):
# read concordances before counting (see --inspect / KWIC).
AMBIGUOUS = {
    "repair", "overlap", "coherence", "progressivity", "next turn",
    "third position", "social action", "face", "accommodation", "stance",
    "common ground", "mutual knowledge", "deixis", "silence", "participation framework",
    "naturalness", "breakdown", "empathy", "engagement", "trust",
}
# Terms that ARE in the sourced lexicon and present in the corpus, but which
# concordance inspection showed are NOT used in the interactional sense. They
# stay in the lists above (so the full searched vocabulary is reported), but are
# subtracted from the validated counts. Value = reason, for the audit trail.
EXCLUDE_AFTER_INSPECTION = {
    "face": "idiom 'face a challenge/limitation', not Goffmanian face",
    "next turn": "system's next action step, not the CA next turn",
    "coherence": "response fluency/quality, not sequential coherence",
    "overlap": "data/feature overlap, not turn overlap",
    "accommodation": "place where someone stays or lives, not linguistic accommodation",
    "politeness": "recommender attribute",
    # add more here as you inspect, e.g.:
    # "trust": "user-attitude evaluation metric, not an interactional phenomenon",
}
# source per layer, for the appendix lexicon table
SOURCES = {
    "CA_core": "Sidnell & Stivers (2012)",
    "pragmatics": "Verschueren & Östman (2022)",
    "hci_cui": "Namvarpour & Razi (2025); Wagner et al. (2025)",
}

# definition cues (surface regex over sentences)
DEF_CUES = re.compile(
    r"\b(is|are)\s+(a|an|the)\b|defined\s+as|refers?\s+to|we\s+define|"
    r"is\s+the\s+task\s+of|is\s+a\s+type\s+of|\bi\.e\.|that\s+is|known\s+as|"
    r"can\s+be\s+(defined|seen|understood)", re.I)
NODE_IN_SENT = re.compile(r"\bconversation\w*|\bdialog\w*", re.I)
# ----------------------------------------------------------------------------


def load_nlp():
    import spacy
    try:
        nlp = spacy.load("en_core_web_sm")
        return nlp, True, f"en_core_web_sm {nlp.meta.get('version','?')}"
    except Exception:
        nlp = spacy.blank("en")
        nlp.add_pipe("sentencizer")
        return nlp, False, "spacy.blank('en') (NO MODEL: surface forms, no POS)"


def find_merged():
    if MERGED_FILE:
        return Path(MERGED_FILE)
    c = sorted(OUT_DIR.glob("merged_scopus_wos_*.csv"))
    if not c:
        sys.exit(f"ERROR: no merged_scopus_wos_*.csv in {OUT_DIR}")
    return c[-1]


def norm(tok):
    """normalised token key: lemma if available, else lowercased surface."""
    lem = tok.lemma_.lower().strip() if tok.lemma_ else ""
    return lem if lem else tok.lower_


def is_node(tok):
    return norm(tok) in NODE_LEMMAS or tok.lower_ in NODE_LEMMAS


def band_of(year):
    try:
        y = int(float(year))
    except Exception:
        return None
    for label, lo, hi in BANDS:
        if lo <= y <= hi:
            return label
    return None


def logdice(cooc, f_node, f_coll):
    return 14 + math.log2(2 * cooc / (f_node + f_coll))


def term_collocates(term, content, window):
    """collocate counts treating `term` as the node (for --inspect)."""
    cc = Counter(); ft = 0
    for stream in content:
        keys = [k for k, _ in stream]
        for pos, (k, _nd) in enumerate(stream):
            if k == term:
                ft += 1
                lo, hi = max(0, pos - window), min(len(keys), pos + window + 1)
                for q in range(lo, hi):
                    if q != pos:
                        cc[keys[q]] += 1
    return ft, cc


def main():
    inspect_terms = []
    if "--inspect" in sys.argv:
        inspect_terms = [t.lower() for t in sys.argv[sys.argv.index("--inspect") + 1:]]
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    nlp, has_model, nlp_desc = load_nlp()
    df = pd.read_csv(find_merged(), dtype=str, encoding="utf-8-sig", keep_default_na=False)

    # build running text per record: title + abstract
    df["text"] = (df["Title"].fillna("") + ". " + df["Abstract"].fillna("")).str.strip()
    df["band"] = df["Year"].map(band_of)

    docs = list(nlp.pipe(df["text"].tolist(), batch_size=64))

    # ---- build per-doc content streams + collect KWIC/definitions/modifiers
    content = []                      # list of list[(key, is_node)]
    kwic_rows, def_rows = [], []
    reg_hit_rows = []                 # paper-level register hits (deviant-case tracing)
    conv_mods = Counter()             # what "conversational" modifies
    node_noun_mods = Counter()        # what modifies conversation/dialogue/interaction
    NODE_NOUNS = {"conversation", "dialogue", "dialog", "interaction"}
    # conversation-family nodes used for the register test (bare 'turn' excluded)
    CONV_FAMILY = {"conversation", "conversational", "dialogue", "dialog",
                   "interaction", "interactive", "chat", "utterance", "multi-turn"}

    for i, doc in enumerate(docs):
        row = df.iloc[i]
        stream = []
        toks = list(doc)
        for j, t in enumerate(toks):
            if t.is_alpha and not t.is_stop:
                stream.append((norm(t), is_node(t)))
            # surface modifier heuristic (works without POS):
            if t.lower_ == "conversational":
                # next alpha token = what it modifies
                if j + 1 < len(toks) and toks[j + 1].is_alpha:
                    conv_mods[norm(toks[j + 1])] += 1
            if norm(t) in NODE_NOUNS:
                if j - 1 >= 0 and toks[j - 1].is_alpha and not toks[j - 1].is_stop:
                    node_noun_mods[(norm(toks[j - 1]), norm(t))] += 1
        # POS/dep refinement when a model is present
        if has_model:
            for t in doc:
                if t.lower_ == "conversational" and t.dep_ == "amod":
                    conv_mods[t.head.lemma_.lower()] += 1
                if t.lemma_.lower() in NODE_NOUNS:
                    for c in t.children:
                        if c.dep_ in ("amod", "compound"):
                            node_noun_mods[(c.lemma_.lower(), t.lemma_.lower())] += 1
        content.append(stream)

        # paper-level register hits: each conversation-family node occurrence,
        # with any instrumental/interactional collocate in its window
        keys = [k for k, _ in stream]
        rid = (row["DOI"].strip() if row["DOI"].strip() else row["Title"][:60])
        for pos, (k, _nd) in enumerate(stream):
            if k in CONV_FAMILY:
                lo, hi = max(0, pos - WINDOW), min(len(stream), pos + WINDOW + 1)
                for q in range(lo, hi):
                    if q == pos:
                        continue
                    ck = keys[q]
                    reg = ("instrumental" if ck in INSTRUMENTAL
                           else "interactional" if ck in INTERACTIONAL_TOKENS else None)
                    if reg:
                        reg_hit_rows.append({
                            "record": rid, "year": row["Year"], "band": row["band"],
                            "node": k, "collocate": ck, "register": reg,
                            "title": row["Title"][:80]})

        # KWIC over raw text
        for m in KWIC_PATTERN.finditer(row["text"]):
            s, e = m.start(), m.end()
            kwic_rows.append({
                "node": m.group(0).lower(), "year": row["Year"], "band": row["band"],
                "left": row["text"][max(0, s - KWIC_CONTEXT):s].replace("\n", " "),
                "hit": m.group(0),
                "right": row["text"][e:e + KWIC_CONTEXT].replace("\n", " "),
                "title": row["Title"][:80],
            })
        # definition sentences
        for sent in doc.sents:
            st = sent.text.strip()
            if NODE_IN_SENT.search(st) and DEF_CUES.search(st) and 5 <= len(st.split()) <= 60:
                def_rows.append({"year": row["Year"], "band": row["band"],
                                 "sentence": st, "title": row["Title"][:80]})

    # ---- corpus-wide frequencies + co-occurrence (overall and per band) -----
    def collocate(indices):
        freq = Counter()
        node_freq = Counter()
        cooc = defaultdict(Counter)
        for idx in indices:
            stream = content[idx]
            keys = [k for k, _ in stream]
            for pos, (k, nd) in enumerate(stream):
                freq[k] += 1
                if nd:
                    node_freq[k] += 1
                    lo, hi = max(0, pos - WINDOW), min(len(stream), pos + WINDOW + 1)
                    for q in range(lo, hi):
                        if q != pos:
                            cooc[k][keys[q]] += 1
        return freq, node_freq, cooc

    all_idx = list(range(len(content)))
    freq, node_freq, cooc = collocate(all_idx)

    # collocation tables per node
    coll_rows = []
    core_nodes = ["conversation", "conversational", "dialogue", "interaction", "chat"]
    for node in NODE_LEMMAS:
        if node not in cooc:
            continue
        fn = node_freq[node]
        for coll, c in cooc[node].items():
            if coll == node or c < MIN_COOC or freq[coll] < MIN_COLL_FREQ:
                continue
            reg = ("instrumental" if coll in INSTRUMENTAL
                   else "interactional" if coll in INTERACTIONAL_TOKENS else "other")
            coll_rows.append({"node": node, "collocate": coll, "cooc": c,
                              "coll_freq": freq[coll],
                              "logDice": round(logdice(c, fn, freq[coll]), 3),
                              "register": reg})
    coll_df = pd.DataFrame(coll_rows).sort_values(["node", "logDice"], ascending=[True, False])
    coll_df.to_csv(OUT_DIR / f"colloc_all_nodes_{RUN_DATE}.csv", index=False)
    for node in core_nodes:
        sub = coll_df[coll_df.node == node]
        if len(sub):
            sub.to_csv(OUT_DIR / f"colloc_{node}_{RUN_DATE}.csv", index=False)

    # ---- register test, computed from paper-level hits ----------------------
    hits_df = pd.DataFrame(reg_hit_rows)
    hits_df.to_csv(OUT_DIR / f"register_hits_{RUN_DATE}.csv", index=False)

    def counts(sub):
        return (int((sub["register"] == "instrumental").sum()),
                int((sub["register"] == "interactional").sum()))

    reg_rows = []
    ai, aintr = counts(hits_df)
    reg_rows.append({"band": "ALL", "instrumental": ai, "interactional": aintr,
                     "n_records": len(df),
                     "instrumental_share": round(ai / (ai + aintr), 3) if (ai + aintr) else None})
    for label, lo, hi in BANDS:
        sub = hits_df[hits_df["band"] == label]
        inst, intr = counts(sub)
        reg_rows.append({"band": label, "instrumental": inst, "interactional": intr,
                         "n_records": int((df["band"] == label).sum()),
                         "instrumental_share": round(inst / (inst + intr), 3) if (inst + intr) else None})
    reg_df = pd.DataFrame(reg_rows)
    reg_df.to_csv(OUT_DIR / f"register_by_band_{RUN_DATE}.csv", index=False)

    # ---- save KWIC / definitions / modifiers --------------------------------
    pd.DataFrame(kwic_rows).to_csv(OUT_DIR / f"kwic_{RUN_DATE}.csv", index=False)
    pd.DataFrame(def_rows).to_csv(OUT_DIR / f"definitions_{RUN_DATE}.csv", index=False)
    pd.DataFrame(sorted(conv_mods.items(), key=lambda x: -x[1]),
                 columns=["modified_noun", "count"]).to_csv(
        OUT_DIR / f"modifiers_conversational_{RUN_DATE}.csv", index=False)
    pd.DataFrame([{"modifier": m, "node_noun": n, "count": c}
                  for (m, n), c in node_noun_mods.most_common()]).to_csv(
        OUT_DIR / f"modifiers_of_node_nouns_{RUN_DATE}.csv", index=False)

    # ---- FIGURE 1: register share per band (100% stacked, comparable) -------
    bands_plot = [r for r in reg_rows if r["band"] != "ALL"]
    labels = [r["band"] for r in bands_plot]
    inst = [r["instrumental"] for r in bands_plot]
    intr = [r["interactional"] for r in bands_plot]
    tot = [a + b for a, b in zip(inst, intr)]
    inst_sh = [100 * a / t if t else 0 for a, t in zip(inst, tot)]
    intr_sh = [100 * b / t if t else 0 for b, t in zip(intr, tot)]
    x = list(range(len(labels)))
    fig, ax = plt.subplots(figsize=(8, 4.8))
    ax.bar(x, inst_sh, 0.6, label="instrumental register", color="#4c78a8")
    ax.bar(x, intr_sh, 0.6, bottom=inst_sh, label="interactional register", color="#e45756")
    ax.set_xticks(x); ax.set_xticklabels(labels, fontsize=9)
    ax.set_ylabel("Share of registered collocate occurrences (%)")
    ax.set_ylim(0, 100)
    for i in x:
        ax.text(i, inst_sh[i] / 2, f"{inst_sh[i]:.0f}%\n(n={inst[i]})",
                ha="center", va="center", color="white", fontsize=8)
        if intr_sh[i] > 4:
            ax.text(i, inst_sh[i] + intr_sh[i] / 2, f"{intr_sh[i]:.0f}%\n(n={intr[i]})",
                    ha="center", va="center", color="white", fontsize=8)
    ax.legend(frameon=False, loc="lower right")
    plt.tight_layout()
    plt.savefig(FIG_DIR / f"fig_register_asymmetry_{RUN_DATE}.png", dpi=150); plt.close()

    # ---- FIGURE 2: collocation network for 'conversational' -----------------
    try:
        import networkx as nx
        node = "conversational"
        sub = coll_df[coll_df.node == node].head(TOP_NETWORK)
        if len(sub):
            G = nx.Graph()
            for _, r in sub.iterrows():
                G.add_edge(node, r["collocate"], weight=r["logDice"], reg=r["register"])
            pos = nx.spring_layout(G, seed=SEED, k=0.6)
            colmap = {"instrumental": "#4c78a8", "interactional": "#e45756", "other": "#bbbbbb"}
            ncolors = [("#222222" if n == node else
                        colmap[G[node][n]["reg"]]) for n in G.nodes()]
            sizes = [1400 if n == node else 500 for n in G.nodes()]
            fig, ax = plt.subplots(figsize=(9, 7))
            nx.draw_networkx_edges(G, pos, alpha=.3, ax=ax)
            nx.draw_networkx_nodes(G, pos, node_color=ncolors, node_size=sizes, ax=ax)
            nx.draw_networkx_labels(G, pos, font_size=9, ax=ax)
            ax.axis("off")
            plt.tight_layout()
            plt.savefig(FIG_DIR / f"fig_colloc_network_conversational_{RUN_DATE}.png", dpi=150)
            plt.close()
    except ImportError:
        print("  (networkx not installed -> skipped collocation network figure)")

    # ---- interactional lexicon presence audit (the 'gradient of absence') ---
    node_spans = [[(m.start(), m.end()) for m in KWIC_PATTERN.finditer(t)]
                  for t in df["text"]]
    audit = []
    for layer, terms in INTERACTIONAL_LEXICON.items():
        for term in sorted(terms):
            pat = re.compile(r"\b" + re.escape(term) + r"\b", re.I)
            nrec = nnear = 0
            for i, t in enumerate(df["text"]):
                ms = [m.start() for m in pat.finditer(t)]
                if not ms:
                    continue
                nrec += 1
                if any(ns[0] - KWIC_CONTEXT <= s <= ns[1] + KWIC_CONTEXT
                       for s in ms for ns in node_spans[i]):
                    nnear += 1
            audit.append({"layer": layer, "term": term, "source": SOURCES.get(layer, ""),
                          "ambiguous": term in AMBIGUOUS,
                          "excluded_after_inspection": term in EXCLUDE_AFTER_INSPECTION,
                          "exclusion_reason": EXCLUDE_AFTER_INSPECTION.get(term, ""),
                          "n_records": nrec, "n_records_near_node": nnear})
    audit_df = pd.DataFrame(audit).sort_values(["layer", "n_records"], ascending=[True, False])
    audit_df.to_csv(OUT_DIR / f"interactional_lexicon_audit_{RUN_DATE}.csv", index=False)
    # validated = present AND not excluded after inspection
    val = audit_df[~audit_df["excluded_after_inspection"]]
    layer_sum = (audit_df.groupby("layer")
                 .agg(terms=("term", "size"),
                      present=("n_records", lambda s: int((s > 0).sum())),
                      record_hits=("n_records", "sum"))
                 .reset_index())
    val_sum = (val.groupby("layer")
               .agg(present_validated=("n_records", lambda s: int((s > 0).sum())),
                    hits_validated=("n_records", "sum")).reset_index())
    layer_sum = layer_sum.merge(val_sum, on="layer", how="left")

    # ---- FIGURE 3: gradient of absence (validated record-hits per layer) ----
    order = ["CA_core", "pragmatics", "hci_cui"]
    nice = {"CA_core": "Conversation analysis\n(interaction-as-object)",
            "pragmatics": "Pragmatics\n(meaning-in-interaction)",
            "hci_cui": "HCI / CUI\n(interaction-as-interface)"}
    ls = layer_sum.set_index("layer").reindex(order)
    vals = [int(ls.loc[l, "hits_validated"]) if l in ls.index else 0 for l in order]
    fig, ax = plt.subplots(figsize=(8, 4.6))
    ax.bar([nice[l] for l in order], vals,
           color=["#e45756", "#f0a35e", "#4c78a8"], width=0.6)
    ax.set_ylabel("Validated record-hits (of 866)")
    for i, v in enumerate(vals):
        ax.text(i, v, str(v), ha="center", va="bottom", fontsize=10)
    ax.spines[["top", "right"]].set_visible(False)
    plt.tight_layout()
    plt.savefig(FIG_DIR / f"fig_interactional_gradient_{RUN_DATE}.png", dpi=150); plt.close()

    # ---- optional: inspect ambiguous terms (--inspect context response turn) -
    if inspect_terms:
        import random
        random.seed(SEED)
        for term in inspect_terms:
            ft, cc = term_collocates(term, content, WINDOW)
            rows = []
            for coll, c in cc.items():
                if coll == term or c < MIN_COOC or freq[coll] < MIN_COLL_FREQ:
                    continue
                reg = ("instrumental" if coll in INSTRUMENTAL
                       else "interactional" if coll in INTERACTIONAL_TOKENS else "other")
                rows.append({"term": term, "collocate": coll, "cooc": c,
                             "coll_freq": freq[coll],
                             "logDice": round(logdice(c, ft, freq[coll]), 3),
                             "register": reg})
            cols = ["term", "collocate", "cooc", "coll_freq", "logDice", "register"]
            cdf = pd.DataFrame(rows, columns=cols)
            if len(cdf):
                cdf = cdf.sort_values("logDice", ascending=False)
            cdf.to_csv(OUT_DIR / f"inspect_colloc_{term}_{RUN_DATE}.csv", index=False)
            pat = re.compile(r"\b" + re.escape(term) + r"\w*\b", re.I)
            lines = []
            for _, row in df.iterrows():
                for m in pat.finditer(row["text"]):
                    s, e = m.start(), m.end()
                    lines.append({"left": row["text"][max(0, s - KWIC_CONTEXT):s].replace("\n", " "),
                                  "hit": m.group(0),
                                  "right": row["text"][e:e + KWIC_CONTEXT].replace("\n", " "),
                                  "title": row["Title"][:80]})
            random.shuffle(lines)
            pd.DataFrame(lines[:40]).to_csv(
                OUT_DIR / f"inspect_kwic_{term}_{RUN_DATE}.csv", index=False)
            ti = sum(r["register"] == "instrumental" for r in rows)
            tx = sum(r["register"] == "interactional" for r in rows)
            print(f"  inspect '{term}': freq {ft}; collocate registers -> "
                  f"instrumental {ti}, interactional {tx}, other {len(rows)-ti-tx} "
                  f"(saved inspect_colloc/inspect_kwic)")

    # ---- summary + run log --------------------------------------------------
    n = len(df)
    allr = reg_rows[0]
    print("Lexical analysis complete.")
    print(f"  NLP: {nlp_desc}")
    print(f"  records: {n} (all kept; 7 non-English retained)")
    print(f"  register mass overall -> instrumental {allr['instrumental']} | "
          f"interactional {allr['interactional']} "
          f"(instrumental share {allr['instrumental_share']})")
    for r in reg_rows[1:]:
        print(f"    {r['band']:24} inst {r['instrumental']:>5} | "
              f"intr {r['interactional']:>4} | share {r['instrumental_share']} | "
              f"n={r.get('n_records','?')}")
    print(f"  register-hit rows (paper-level): {len(hits_df)}  -> register_hits_{RUN_DATE}.csv")
    print("  interactional lexicon audit (gradient of absence):")
    for _, r in layer_sum.iterrows():
        print(f"    {r['layer']:10} terms={r['terms']:>2} "
              f"present={r['present']:>2} (validated={int(r['present_validated'])}) "
              f"hits={r['record_hits']} (validated={int(r['hits_validated'])})")
    if EXCLUDE_AFTER_INSPECTION:
        print(f"  excluded after inspection: {', '.join(sorted(EXCLUDE_AFTER_INSPECTION))}")
    print(f"  KWIC lines: {len(kwic_rows)} | definition sentences: {len(def_rows)}")
    print(f"  figures + tables -> {OUT_DIR}")

    log = log_run(__file__,
                  inputs=[str(find_merged())],
                  outputs=[str(OUT_DIR / f"colloc_all_nodes_{RUN_DATE}.csv"),
                           str(OUT_DIR / f"register_by_band_{RUN_DATE}.csv"),
                           str(OUT_DIR / f"register_hits_{RUN_DATE}.csv"),
                           str(OUT_DIR / f"interactional_lexicon_audit_{RUN_DATE}.csv"),
                           str(FIG_DIR / f"fig_register_asymmetry_{RUN_DATE}.png"),
                           str(OUT_DIR / f"kwic_{RUN_DATE}.csv"),
                           str(OUT_DIR / f"definitions_{RUN_DATE}.csv")],
                  params=f"window=±{WINDOW}, min_cooc={MIN_COOC}, min_coll_freq={MIN_COLL_FREQ}, "
                         f"bands={[b[0] for b in BANDS]}, nlp={nlp_desc}",
                  notes=f"{n} records; instrumental/interactional overall = "
                        f"{allr['instrumental']}/{allr['interactional']}")
    print(f"  run log -> {log}")


if __name__ == "__main__":
    main()
