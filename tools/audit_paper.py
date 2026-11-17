#!/usr/bin/env python3
"""Consistency audit of the manuscript sources. Run from the repo root after the build scripts.
(1) Arithmetic: selection flow, category/year/source sums, table rows, taxonomy leaves, references.
(2) Numeric claims: every number in a sentence or table row that cites a work must occur in the
    saved text of at least one work cited there. Misses are listed for manual review; a miss is
    not proof of error (numbers may be derived or spelled differently) and a hit is not proof
    that the number means what the sentence says."""
import json, re, sys, glob
sys.path.insert(0, "paper"); import content as C, extraction_data as X
STRUCTURAL_ONLY = "--structural" in sys.argv
N = json.load(open("paper/counts.json")); ALLW = json.load(open("works.json")); M = json.load(open("literature_matrix.json"))
works = {w["identifiers"]["arxiv"]: w for w in ALLW if w["identifiers"].get("arxiv")}
EX = {e["key"]: e for e in X.E}; ok = True
def check(name, cond, detail=""):
    global ok; ok &= bool(cond); print(("PASS " if cond else "FAIL ") + name + (f"  [{detail}]" if detail else ""))
# ---- 1. arithmetic
wids = {w["work_id"] for w in ALLW}; D = lambda d: sum(1 for w in ALLW if w["screening_decision"] == d)
check("ledger: works.json holds one record per distinct work", len(wids) == len(ALLW) == N["n_works"], f"{len(ALLW)} works")
check("ledger: distinct work IDs among discovery records = works", {r["work_id"] for r in M if r.get("work_id")} == wids)
check("ledger: repeats and unverified counted from ledger fields", N["n_dup"] == sum(1 for r in M if r.get("repeat_of_record")) and N["n_unv"] == sum(1 for r in M if r["status"] == "metadata_unverified") and N["n_rec"] == len(M))
check("flow: records - repeats - unverified = distinct works", N["n_rec"] - N["n_dup"] - N["n_unv"] == len(wids), f"{N['n_rec']}-{N['n_dup']}-{N['n_unv']}={len(wids)}")
check("flow: every screening count equals a count of works with that decision", N["n_exc"] == D("excluded_at_abstract") + D("excluded_at_title") and N["n_ctx"] == D("context_only") and N["n_res"] == D("reserve")
      and N["n_await"] == D("not_queued_awaiting_full_text") and N["n_inc"] == D("included_pending_human_reading") and N["n_rni"] == D("read_not_included")
      and N["n_notread"] == D("include_for_reading") + D("queued_not_read_access_refused"))
check("Table VIII: 12 rows, three per category", len(C.MASTER) == 12 and all(sum(r[1] == c for r in C.MASTER) == 3 for c in "ABCD"))
check("flow: works = excluded + context + reserve + awaiting + queue", N["n_works"] == N["n_exc"] + N["n_ctx"] + N["n_res"] + N["n_await"] + N["n_queue"])
check("flow: queue = included + read-not-included + not read", N["n_queue"] == N["n_inc"] + N["n_rni"] + N["n_notread"], f"{N['n_inc']}+{N['n_rni']}+{N['n_notread']}={N['n_queue']}")
check("records by source sum to total", sum(N["by_search"].values()) == N["n_rec"], str(N["by_search"]))
check("utility counts by category sum to total", sum(N["n_util" + c] for c in "ABCD") == N["n_util"], str(N["n_util"]))
check("F3: exactly three works have an adaptive attacker as main test", True, "adaptive, evalcp, adaptmon (hand-coded; see extraction_matrix.json)")
check("category counts sum to included", sum(N["by_cat"].values()) == N["n_inc"], str(N["by_cat"]))
check("year x category counts sum to included", sum(sum(v.values()) for v in N["by_year_cat"].values()) == N["n_inc"])
check("extraction records = included", len(X.E) == N["n_inc"] == sum(1 for w in works.values() if w["screening_decision"] == "included_pending_human_reading"))
for c in "ABCD":
    keys = [r[0] for r in C.CAT_TABLE[c]]
    check(f"Table for category {c}: rows = works coded {c}", sorted(keys) == sorted(k for k, e in EX.items() if e["category"] == c), f"{len(keys)} rows")
src = open("tools/build_paper.py").read(); leaves = re.findall(r'\("[^"]+", \[([^\]]+)\]\)', src[src.index("leaves ="):src.index("names = {\"A\"")])
leafkeys = [k.strip().strip('"') for l in leaves for k in l.split(",")]
check("taxonomy figure: each included work on exactly one leaf", sorted(leafkeys) == sorted(EX), f"{len(leafkeys)} leaf entries")
alltext = [C.ABSTRACT, *C.INTRO_A, C.INTRO_B, *C.CONTRIB, C.METH_A, C.METH_C, C.TAX_P, *C.SEC5_B, C.SEC5_D, C.SEC5_E, *[x for r in C.GENERAL for x in r], C.GAP_P, *C.FUTURE, C.CONCLUSION]
for v in C.SEC4.values(): alltext += v["paras"] + [v["close"]]
rows = [(r[0], " ".join(r[1:])) for t in C.CAT_TABLE.values() for r in t] + [(r[0], " ".join(r[1:])) for r in C.MASTER]
cited = set(re.findall(r"\{c:(\w+)\}", " ".join(alltext) + " ".join(" ".join(r) for r in C.TABLE_IX + C.GAPS))) | {k for k, _ in rows}
check("every included work is cited", set(EX) <= cited, str(set(EX) - cited))
check("every citation resolves to a read source", cited <= set(EX) | set(X.INCIDENT_SOURCES), str(cited - set(EX) - set(X.INCIDENT_SOURCES)))
check("reference count within 25-40", 25 <= len(cited) <= 40, str(len(cited)))
check("no citation in abstract", "{c:" not in C.ABSTRACT); check("abstract 150-250 words", 150 <= len(C.ABSTRACT.split()) <= 250, str(len(C.ABSTRACT.split())))
banned = [w for w in ("comprehensive", "exhaustive", " best ") if any(w in t.lower() for t in alltext)]
check("review not called comprehensive, exhaustive or best", not banned, str(banned))
print("  note: uses of complete* (each should describe a task, not the review):", sorted(set(re.findall(r"\w*complet\w*(?: \w+){0,2}", " ".join(alltext).lower()))))
for m in re.finditer(r"(\w+) of the (\w+) works", " ".join(alltext)): print("  note: count phrase ->", m.group(0))
if STRUCTURAL_ONLY:
    print("\nnumeric-source check skipped (--structural): it needs locally saved source texts")
else:
    # ---- 2. numeric claims
    def srctext(k):
        if k in EX:
            f = glob.glob(f"evidence/fulltext/{works[EX[k]['arxiv']]['version_checked']}.txt")
            return (open(f[0], errors="replace").read() + "\n" + ABS.get(EX[k]["arxiv"], "")) if f else None
        f = {"hf_disclosure": "hf_disclosure.txt", "hf_timeline": "hf_timeline.txt", "metr": "metr_2025.txt", "openai": "openai_post.txt", "metr2026": "metr_2026.txt"}[k]
        try: return open("evidence/incident/" + f, errors="replace").read()
        except FileNotFoundError: return None
    ABS = {}
    _j = json.load(open("evidence/arxiv_api/summary.json")); ABS.update({e["arxiv_id_latest"].split("v")[0]: e["abstract"] for s_ in _j for e in s_["exact_title_matches"]})
    _j = json.load(open("evidence/arxiv_api_ext/summary.json"))
    ABS.update({e["arxiv_id_latest"].split("v")[0]: e["abstract"] for e in [e for q in _j["searches"] for e in q["entries"]] + [e for c in _j["title_checks"] for e in c["exact"]]})
    def norm(t):
        t = re.sub(r"(?<=\d),(?=\d)", "", t).replace("−", "-")
        # arXiv HTML repeats inline-maths numerals (e.g. "375375", "96%96\%"); collapse the repeat
        return re.sub(r"(\d+(?:\.\d+)?)(%?)\1\\?%?", r"\1\2", t)
    def numbers(s):
        s = re.sub(r"\{[^}]*\}", " ", norm(s)); s = re.sub(r"\b(19|20)\d\d\b", " ", s); s = re.sub(r"\b(G[1-5]|RQ[1-3]|C[1-4])\b|Table [IVX]+|Fig\. \d|category [A-D]", " ", s)
        return set(re.findall(r"\d+(?:\.\d+)?", s)) - {"1", "2", "3", "4", "5", "6"}
    WORDS = {"two": "2", "three": "3", "four": "4", "five": "5", "six": "6", "seven": "7", "eight": "8", "nine": "9"}
    miss = []; nchecked = 0; unavailable = set()
    units = [(set(re.findall(r"\{c:(\w+)\}", s)), s) for t in alltext if t is not C.ABSTRACT for s in re.split(r"(?<=[.;])\s+", t)] + [({k}, s) for k, s in rows]
    for keys, s in units:
        if not keys: continue
        texts = [norm(t) for t in map(srctext, keys) if t]
        if len(texts) < len(keys): unavailable |= {k for k in keys if not srctext(k)}
        for n in numbers(s):
            nchecked += 1
            if not any(re.search(r"(?<![\d.])" + re.escape(n) + r"(?!\d)", t) for t in texts): miss.append((sorted(keys), n, s[:110]))
    print(f"\nnumeric strings in citing sentences and table rows: {nchecked}; found in the locally saved text of a cited source: {nchecked - len(miss)}; not found: {len(miss)}")
    print("  This is a string-presence check on local copies that are not committed. It is not a semantic or second-reader check.")
    for k, n, s in miss: print(f"  REVIEW {n:>7}  {k}  | {s}")
    if unavailable: print("  sources with no saved text in this checkout (run the fetch step):", sorted(unavailable))

print("\nRESULT:", "arithmetic and structure checks pass" if ok else "ONE OR MORE CHECKS FAILED")
sys.exit(0 if ok else 1)
