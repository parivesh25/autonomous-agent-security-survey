#!/usr/bin/env python3
"""T01 metadata verification: query the arXiv API by exact title for each
discovery record and save the raw Atom response as a receipt.

Usage: python3 tools/verify_arxiv.py literature_matrix.json evidence/arxiv_api
Output: evidence/arxiv_api/<ID>.xml (raw) and evidence/arxiv_api/summary.json
A title match is a lead for human confirmation, not an inclusion decision.
"""
import json, re, sys, time, urllib.parse, urllib.request
import xml.etree.ElementTree as ET

NS = {"a": "http://www.w3.org/2005/Atom", "x": "http://arxiv.org/schemas/atom"}
norm = lambda s: re.sub(r"[^a-z0-9]", "", s.lower())

def query(title):
    words = re.sub(r"[^A-Za-z0-9 ]", " ", title)
    q = 'ti:"%s"' % " ".join(words.split())
    url = "https://export.arxiv.org/api/query?" + urllib.parse.urlencode(
        {"search_query": q, "max_results": 5})
    for attempt in range(4):
        try:
            with urllib.request.urlopen(url, timeout=60) as r:
                return url, r.read()
        except Exception as e:  # network errors: back off and retry
            err = e
            time.sleep(5 * (attempt + 1))
    raise err

def parse(raw):
    out = []
    for e in ET.fromstring(raw).findall("a:entry", NS):
        g = lambda p: (e.findtext(p, default=None, namespaces=NS) or None)
        out.append({
            "arxiv_id_latest": g("a:id").rsplit("/", 1)[-1],
            "title": " ".join(g("a:title").split()),
            "authors": [a.findtext("a:name", namespaces=NS) for a in e.findall("a:author", NS)],
            "first_submitted": g("a:published"),
            "latest_version_date": g("a:updated"),
            "primary_category": e.find("x:primary_category", NS).get("term"),
            "journal_ref": g("x:journal_ref"),
            "doi": g("x:doi"),
            "comment": g("x:comment"),
            "abstract": " ".join(g("a:summary").split()),
        })
    return out

def main(matrix, outdir):
    summary = []
    for r in json.load(open(matrix)):
        title = " ".join(r["title"].split())
        url, raw = query(title)
        open(f"{outdir}/{r['id']}.xml", "wb").write(raw)
        entries = parse(raw)
        exact = [e for e in entries if norm(e["title"]) == norm(title)]
        summary.append({"id": r["id"], "discovery_title": title, "query_url": url,
                        "returned": len(entries), "exact_title_matches": exact,
                        "other_returned_titles": [e["title"] for e in entries if e not in exact]})
        print(r["id"], len(entries), [e["arxiv_id_latest"] for e in exact], flush=True)
        time.sleep(3.2)  # arXiv API etiquette
    json.dump(summary, open(f"{outdir}/summary.json", "w"), indent=1, ensure_ascii=False)

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
