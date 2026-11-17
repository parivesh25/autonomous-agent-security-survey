#!/usr/bin/env python3
"""T02-T05 ledger build: extraction matrix, incident ledger, publisher-filtered Crossref records,
search-log additions, selection counts and the three figures. Run from the repo root."""
import json, re, sys, glob, collections
sys.path.insert(0, "paper"); sys.path.insert(0, "tools")
import extraction_data as X
TODAY = "2026-11-16"
norm = lambda s: re.sub(r"[^a-z0-9]", "", re.sub(r"<[^>]+>|&amp;", "", s).lower())
works = json.load(open("works.json")); byax = {w["identifiers"]["arxiv"]: w for w in works}
matrix = [r for r in json.load(open("literature_matrix.json")) if not r["search_id"].startswith("D")]
log = [s for s in json.load(open("search_log.json")) if not re.match(r"[DX]\d", s["search_id"])]

# ---- 1. extraction matrix + works update
ext = []
for e in X.E:
    w = byax[e["arxiv"]]
    rec = dict(work_id=w["work_id"], title=w["title"], version_read=w["version_checked"], version_date=w["version_date"],
               source_url=f"https://arxiv.org/html/{w['version_checked']}" if e["key"] != "chess" else f"https://arxiv.org/pdf/{w['version_checked']}",
               read_by="AI reviewer claude-t02", read_date=TODAY, human_reading_status=None, second_reader_check=None, **e)
    ext.append(rec)
    w.update(gate=6, screening_decision="included_pending_human_reading", full_text_read=True,
             proposed_primary_category=e["category"], secondary_tags=e["secondary"], proposed_behaviour_source=e["behaviour_source"],
             coding_status="coded from full text by one AI reviewer; second-reader check pending",
             agent_reading_status=f"sections read {TODAY} at {w['version_checked']}: {e['sections_read']}",
             extraction=f"extraction_matrix.json#{e['key']}")
for ax, (why, secs) in X.READ_NOT_INCLUDED.items():
    byax[ax].update(gate=5, screening_decision="read_not_included", full_text_read=True, screening_reason=why,
        agent_reading_status=f"read at reduced depth {TODAY} at {byax[ax]['version_checked']}: {secs}", coding_status="not extracted")
for r in matrix:
    if r["id"] == "P011": r.update(status="awaiting_full_text", screening_reason=X.NOT_READ["P011"])
for r in matrix:
    w = next((x for x in works if x["work_id"] == r.get("work_id")), None)
    if w and w["full_text_read"] and r["status"] not in ("duplicate",):
        r.update(status=w["screening_decision"], full_text_read=True, category=w["proposed_primary_category"])
json.dump(ext, open("extraction_matrix.json", "w"), indent=1, ensure_ascii=False)
json.dump(dict(sources=X.INCIDENT_SOURCES, claims=X.INCIDENT,
               note="T05 ledger. Claims are attributed to the named report and date. The two Hugging Face posts are one party's account, not independent replications."),
          open("incident_claim_ledger.json", "w"), indent=1, ensure_ascii=False)

# ---- 2. publisher-filtered Crossref records (D1-D9)
known = {norm(w["title"]): w["work_id"] for w in works}
known.update({norm(r["title"]): r["id"] for r in matrix if not r.get("work_id")})
plog = json.load(open("evidence/db_search/crossref_publisher_log.json")); n = len(matrix); seen = {}
for k, q in enumerate(plog, 1):
    sid = f"D{k}"; f = f"evidence/db_search/crossref_{q['pub']}_{'abc'[(k-1)%3]}.json"
    items = json.load(open(f))["message"]["items"]
    for it in items:
        n += 1; t = " ".join(re.sub(r"<[^>]+>", "", (it.get("title") or ["(untitled)"])[0]).split()); nt = norm(t)
        rep = seen.get(nt); wk = known.get(nt)
        status = "repeat_within_crossref" if rep else ("published_record_of_known_work" if wk else "title_screened_not_selected")
        matrix.append({"id": f"P{n:03d}", "search_id": sid, "title": t, "scispace_id": None, "url": "https://doi.org/" + it["DOI"], "discovery_excerpt": None,
            "status": status, "possible_duplicate_of": None, "primary_url": "https://doi.org/" + it["DOI"], "publication_date_verified": True, "full_text_read": False,
            "category": None, "screening_reason": ("Same DOI/title as %s." % rep if rep else "Matches %s already in the ledger." % wk if wk else
                "Title-level screen of a publisher-filtered Crossref result; not added to the reading queue (capacity; see handoff)."),
            "methods": None, "testbed": None, "metric_definition": None, "denominator": None, "findings": None, "limitations": None, "evidence_locator": f,
            "work_id": wk if wk and wk.startswith("W") else None, "venue": (it.get("container-title") or [None])[0], "record_type": it.get("type")})
        if rep or wk: matrix[-1]["repeat_discovery_of"] = rep or wk
        seen.setdefault(nt, f"P{n:03d}")
    log.append({"search_id": sid, "executed_date": TODAY, "source": f"Crossref REST API, filter member = {q['pub']}", "query": f"query.bibliographic=\"{q['q']}\"; from-pub-date 2023-01-01; until-pub-date 2026-11-16",
        "retrieval_limit": 10, "returned_count": q["returned"], "total_database_hits": q["total"], "status": "fulfilled",
        "notes": "Publisher-filtered Crossref query, NOT a native search of the publisher's own database. total_database_hits is Crossref's relevance-ranked match count for loosely related terms and must not be read as the number of relevant papers."})
for sid, src, q, note in [
 ("X1", "IEEE Xplore, ACM Digital Library, SpringerLink (native interfaces)", "not executed", "A scripted request to IEEE Xplore's internal search endpoint was blocked by the session's safety policy and not retried; ACM and SpringerLink native searches were not attempted afterwards. Replaced by D1-D9. A team member with institute access should run and log native searches."),
 ("X2", "Google Scholar; Reddit", "not executed", "The hosts could not be added to this session's network allowlist (the change was rejected twice). Not searched."),
 ("X3", "Web search (general)", "OpenAI Hugging Face incident autonomous agent unauthorized 2026", "Used only to locate primary report URLs. Search-engine summaries are not evidence and are not cited."),
 ("X4", "Web search restricted to metr.org", "METR reward hacking frontier models report", "Used only to locate report URLs; the 2025-06-05 report was then opened at metr.org."),
 ("X5", "openai.com", "https://openai.com/index/hugging-face-model-evaluation-security-incident/", "HTTP 403 to automated requests (direct and via fetch tool). This earlier operator post was NOT read. The operator's 26 Aug 2026 summary report was later read from a saved copy supplied by the student (ledger I15)."),
 ("X7", "metr.org", "https://metr.org/blog/2026-08-26-openai-hugging-face-incident-investigation/", "Retrieved directly; sections read are listed in incident_claim_ledger.json."),
 ("X8", "YouTube (Black Hat USA 2026 talk)", "not executed", "Video host outside the network allowlist; no transcript available. Not accessed."),
 ("X9", "www.mdpi.com", "https://www.mdpi.com/2073-431X/15/9/570/htm", "HTTP 403 to automated requests; P011 remains awaiting full text."),
 ("X6", "huggingface.co; en.wikipedia.org; metr.org", "direct retrieval of three primary reports and one tertiary article", "See incident_claim_ledger.json for what was read."),
]:
    log.append({"search_id": sid, "executed_date": TODAY, "source": src, "query": q, "retrieval_limit": None, "returned_count": 0, "total_database_hits": None,
                "status": "not_executed" if q == "not executed" else "fulfilled", "notes": note})
json.dump(matrix, open("literature_matrix.json", "w"), indent=1, ensure_ascii=False)
# published-version lookup (Crossref exact-title match, non-preprint record); absence is not evidence of non-publication
try:
    V = json.load(open("evidence/venue_check/summary.json"))
    for e in X.E:
        v = V.get(e["key"], {}); w = byax[e["arxiv"]]
        if v.get("status") == "published_record_found":
            w.update(published_record={"doi": v["doi"], "container": v["container"].replace("&amp;", "&"), "year": v["year"], "type": v["type"], "basis": "Crossref exact-title match, 2026-11-17; publisher page not opened"},
                     peer_review_status="published record found in Crossref (venue's review process not assessed)")
        else: w["published_record"] = None
except FileNotFoundError: pass
json.dump(works, open("works.json", "w"), indent=1, ensure_ascii=False)
json.dump(log, open("search_log.json", "w"), indent=1, ensure_ascii=False)

# ---- 3. selection counts
C = collections.Counter
st = C(r["status"] for r in matrix)
dup = sum(1 for r in matrix if r.get("repeat_discovery_of") or r["status"] == "duplicate")
unv = st["metadata_unverified"]
crossref_new = st["title_screened_not_selected"]
wd = C(w["screening_decision"] for w in works)
nonarx = {r["id"]: r["status"] for r in matrix if r.get("metadata_basis")}
counts = dict(n_rec=len(matrix), n_dup=dup, n_unv=unv, n_works=len(matrix) - dup - unv,
    n_exc=wd["excluded_at_abstract"] + crossref_new, n_ctx=wd["context_only"] + 1, n_res=wd["reserve"] + 1, n_await=1,
    n_inc=wd["included_pending_human_reading"], n_rni=wd["read_not_included"], n_notread=wd["include_for_reading"] + 1,
    by_search=dict(C(re.sub(r"\d+$", "", r["search_id"]) for r in matrix)),
    by_cat=dict(sorted(C(e["category"] for e in X.E).items())),
    by_year_cat={y: dict(sorted(C(e["category"] for e in X.E if byax[e["arxiv"]]["first_public_date"][:4] == y).items())) for y in ("2023", "2024", "2025", "2026")},
    by_source=dict(C(e["behaviour_source"] for e in X.E)))
counts["n_queue"] = counts["n_inc"] + counts["n_rni"] + counts["n_notread"]
for c in "ABCD": counts["n_cat" + c] = counts["by_cat"][c]
counts["n_util"] = sum(1 for e in X.E if e["utility"])
for c in "ABCD": counts["n_util" + c] = sum(1 for e in X.E if e["utility"] and e["category"] == c)
counts["n_a26"] = counts["by_year_cat"]["2026"].get("A", 0); counts["n_c26"] = counts["by_year_cat"]["2026"].get("C", 0)
assert sum(counts["by_cat"].values()) == counts["n_inc"] == sum(sum(v.values()) for v in counts["by_year_cat"].values()) == sum(counts["by_source"].values())
assert counts["n_works"] == counts["n_exc"] + counts["n_ctx"] + counts["n_res"] + counts["n_await"] + counts["n_queue"], counts
json.dump(counts, open("paper/counts.json", "w"), indent=1); print(json.dumps(counts, indent=1))
