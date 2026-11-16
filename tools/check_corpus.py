#!/usr/bin/env python3
"""Read-only audit of the ledgers (Python counterpart of check_corpus.ps1)."""
import json, collections, sys
m = json.load(open("literature_matrix.json")); log = json.load(open("search_log.json")); works = json.load(open("works.json"))
ids = [r["id"] for r in m]; assert len(ids) == len(set(ids)), "duplicate record IDs"
for s in log:
    n = sum(r["search_id"] == s["search_id"] for r in m)
    assert n == s["returned_count"], f"search count mismatch {s['search_id']}: {n} vs {s['returned_count']}"
wid = {w["work_id"] for w in works}
assert all(r["work_id"] in wid for r in m if r.get("work_id")), "broken work reference"
assert all(r["possible_duplicate_of"] in ids for r in m if r["possible_duplicate_of"]), "broken duplicate reference"
assert not any(w["full_text_read"] for w in works) and not any(r["full_text_read"] for r in m)
C = collections.Counter
dec = lambda d: [w for w in works if w["screening_decision"] == d]
rep = {
 "discovery_records": len(m), "records_by_search": dict(C(r["search_id"] for r in m)),
 "record_status": dict(C(r["status"] for r in m)),
 "repeat_or_duplicate_records": sum(1 for r in m if r.get("repeat_discovery_of") or r["status"] == "duplicate"),
 "records_without_verified_primary_record": [r["id"] for r in m if r["status"] == "metadata_unverified"],
 "non_arxiv_records_verified_via_crossref": [r["id"] for r in m if r.get("metadata_basis")],
 "unique_arxiv_works": len(works), "work_screening_decisions": dict(C(w["screening_decision"] for w in works)),
 "include_for_reading_by_category": dict(sorted(C(str(w["proposed_primary_category"]) for w in dec("include_for_reading")).items())),
 "include_for_reading_by_first_public_year": dict(sorted(C(w["first_public_date"][:4] for w in dec("include_for_reading")).items())),
 "reserve_by_category": dict(sorted(C(str(w["proposed_primary_category"]) for w in dec("reserve")).items())),
 "works_outside_window": [(w["work_id"], w["first_public_date"]) for w in works if not w["in_review_window"]],
 "works_past_cutoff": [w["work_id"] for w in works if not w["within_evidence_cutoff"]],
 "full_text_read_works": 0, "included_works": 0,
 "caveat": "Gate 4 (abstract screened) only. No work is read in full or included. Year/category counts describe a reading queue, not the field and not the final corpus.",
}
json.dump(rep, sys.stdout, indent=1); print()
