#!/usr/bin/env python3
"""Read-only audit of the ledgers (Python counterpart of check_corpus.ps1)."""
import json, collections, sys
m = json.load(open("literature_matrix.json")); log = json.load(open("search_log.json")); works = json.load(open("works.json"))
ids = [r["id"] for r in m]; assert len(ids) == len(set(ids)), "duplicate record IDs"
for s in log:
    n = sum(r["search_id"] == s["search_id"] for r in m)
    assert n == s["returned_count"], f"search count mismatch {s['search_id']}: {n} vs {s['returned_count']}"
wid = {w["work_id"] for w in works}; rid = set(ids); byid = {r["id"]: r for r in m}
assert len(wid) == len(works), "duplicate work IDs"
# every link field has one namespace and a valid target
for r in m:
    assert r.get("work_id") is None or r["work_id"] in wid, f"{r['id']}: work_id not in works.json"
    for f in ("possible_duplicate_of", "repeat_of_record"):
        assert r.get(f) is None or (r[f] in rid and r[f] != r["id"]), f"{r['id']}: {f} is not another record ID"
    assert "repeat_discovery_of" not in r, f"{r['id']}: legacy mixed-namespace field present"
    if r.get("repeat_of_record"):
        assert byid[r["repeat_of_record"]].get("work_id") == r["work_id"], f"{r['id']}: repeat link crosses works"
        assert not byid[r["repeat_of_record"]].get("repeat_of_record"), f"{r['id']}: repeat link does not point to a canonical record"
    assert (r.get("work_id") is None) == (r["status"] == "metadata_unverified"), f"{r['id']}: verified record without a work, or unverified record with one"
# one canonical record per work, and the selection arithmetic by distinct work ID
canon = [r for r in m if r.get("work_id") and not r.get("repeat_of_record")]
assert sorted(r["work_id"] for r in canon) == sorted(wid), "works and canonical records are not one-to-one"
for w in works:
    assert w["canonical_record_id"] in rid and byid[w["canonical_record_id"]]["work_id"] == w["work_id"], f"{w['work_id']}: bad canonical record"
    assert sorted(w["discovery_record_ids"]) == sorted(r["id"] for r in m if r.get("work_id") == w["work_id"]), f"{w['work_id']}: record list out of date"
n_rep = sum(1 for r in m if r.get("repeat_of_record")); n_unv = sum(1 for r in m if r["status"] == "metadata_unverified")
assert len(m) - n_rep - n_unv == len(wid), "records - repeats - unverified != distinct works"
C = collections.Counter
dec = lambda d: [w for w in works if w["screening_decision"] == d]
rep = {
 "discovery_records": len(m), "records_by_search": dict(C(r["search_id"] for r in m)),
 "record_status": dict(C(r["status"] for r in m)),
 "repeat_records": n_rep, "unverified_records": n_unv, "distinct_works": len(wid),
 "records_without_verified_primary_record": [r["id"] for r in m if r["status"] == "metadata_unverified"],
 "non_arxiv_records_verified_via_crossref": [r["id"] for r in m if r.get("metadata_basis")],
 "works_with_arxiv_id": sum(1 for w in works if w["identifiers"].get("arxiv")), "works_without_arxiv_id": sum(1 for w in works if not w["identifiers"].get("arxiv")), "work_screening_decisions": dict(C(w["screening_decision"] for w in works)),
 "included_by_category": dict(sorted(C(str(w["proposed_primary_category"]) for w in dec("included_pending_human_reading")).items())),
 "included_by_first_public_year": dict(sorted(C((w["first_public_date"] or "?")[:4] for w in dec("included_pending_human_reading")).items())),
 "reserve_by_category": dict(sorted(C(str(w["proposed_primary_category"]) for w in dec("reserve")).items())),
 "works_outside_window": [(w["work_id"], w["first_public_date"]) for w in works if not w["in_review_window"]],
 "works_past_cutoff": [w["work_id"] for w in works if not w["within_evidence_cutoff"]],
 "full_text_read_by_ai_reviewer": sum(w["full_text_read"] for w in works), "human_reading_confirmed": sum(1 for w in works if w["human_reading_status"]),
 "caveat": "Full-text reading so far is by an AI reviewer only; no human reading or second-reader check is recorded. Counts describe this corpus, not the field.",
}
json.dump(rep, sys.stdout, indent=1); print()
