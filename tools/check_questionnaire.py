#!/usr/bin/env python3
"""Consistency check of the questionnaire exports. Run from the repo root.
Fails if the CSV, codebook and JSON disagree, or if the responses template holds any row."""
import csv, json, os, sys
J = json.load(open("survey/questionnaire.json")); Q = J["questions"]
form = list(csv.DictReader(open("survey/questionnaire.csv", encoding="utf-8")))
book = list(csv.DictReader(open("survey/codebook.csv", encoding="utf-8")))
tmpl = list(csv.reader(open("survey/responses_template.csv", encoding="utf-8")))
def n_opts(q): return len(q["options"]) if q["type"] in ("single", "multi") else len(q["items"]) if q["type"] in ("bestworst", "likert") else 1
def n_cols(q): return 1 if q["type"] in ("single", "text") else len(q["options"]) if q["type"] == "multi" else 2 if q["type"] == "bestworst" else len(q["items"])
checks = [
 ("item count matches metadata", len(Q) == J["meta"]["n_items"] and sum(q["type"] != "text" for q in Q) == J["meta"]["n_closed"]),
 ("item IDs are unique", len({q["id"] for q in Q}) == len(Q)),
 ("CSV has one row per answer option", len(form) == sum(n_opts(q) for q in Q)),
 ("CSV items match JSON items in order", [q["id"] for q in Q] == list(dict.fromkeys(r["item_id"] for r in form))),
 ("codebook has one row per response column", len(book) == 2 + sum(n_cols(q) for q in Q) and len({b["response_column"] for b in book}) == len(book)),
 ("responses template header equals codebook columns", len(tmpl) >= 1 and tmpl[0] == [b["response_column"] for b in book]),
 ("responses template holds no answer rows", len(tmpl) == 1),
 ("no responses directory with files", not (os.path.isdir("survey/responses") and os.listdir("survey/responses"))),
 ("every most/least item offers at least four options", all(len(q["items"]) >= 4 for q in Q if q["type"] == "bestworst")),
 ("status says not administered", "not administered" in J["meta"]["status"]),
]
ok = True
for name, cond in checks:
    ok &= bool(cond); print(("PASS " if cond else "FAIL ") + name)
print(f"{len(Q)} items, {len(form)} option rows, {len(book)} response columns, {len(tmpl) - 1} answer rows")
sys.exit(0 if ok else 1)
