#!/usr/bin/env python3
"""Build T01 deliverables from saved API receipts plus the reviewer's
screening decisions below. Re-runnable; reads only files in the repo.
Run from the repository root: python3 tools/build_t01.py
"""
import json, re, sys
sys.path.insert(0, "tools")
from verify_arxiv import parse

TODAY = "2026-11-16"
base = lambda i: re.sub(r"v\d+$", "", i)
# decision codes: read = include for full-text reading (core queue); reserve = eligible on
# abstract, read if coverage/capacity requires; context = review/position/foundational, not a
# primary finding source; exclude = out of scope on abstract.
# value: (decision, primary_category, secondary_tags, behaviour_source, reason)
EXT, RT, ENDO, MIX = "external attacker", "prompted red-team agent", "endogenous optimization", "mixed/unclear"
RLHF = "Reward-model over-optimisation during RLHF/RLVR/DPO training or decoding; abstract describes no agent action channel (protocol exclusion: no agent-action relevance)."
D = {
 # pilot S1-S3
 "2605.02964": ("read", "A", [], ENDO, "Benchmark of shortcut/tampering opportunities for tool-using agents; empirical."),
 "2406.10162": ("read", "A", [], ENDO, "Seed study: curriculum from specification gaming to reward tampering."),
 "2603.11337": ("read", "A", [], MIX, "Evaluator tampering and train/test leakage in ML-engineering agent workspaces; abstract reports scripted attacks plus agent runs."),
 "2606.15385": ("read", "A", [], ENDO, "Text adaptation of AI Safety Gridworlds; observed vs hidden objective."),
 "2607.22368": ("read", "A", [], ENDO, "Audit procedure for benchmark protocol validity and score inflation."),
 "2609.28614": ("read", "A", ["D"], MIX, "Reward hacking by research agents and its detectability by a review panel; both spontaneous and permitted-hacking conditions."),
 "2605.02269": ("read", "A", [], ENDO, "Task suite measuring specification gaming across models and mitigations."),
 "2511.21654": ("read", "A", [], ENDO, "Reward-hacking benchmark for coding agents with three detection methods."),
 "2604.03870": ("read", "B", [], EXT, "Defences vs indirect prompt injection in multi-step tool-calling environments."),
 "2604.10134": ("reserve", "B", [], EXT, "Single defence proposal (planner-based verification); read if defence coverage is thin."),
 "2605.17986": ("read", "B", [], EXT, "Injection benchmark on a live but test-controlled VM; relevant to RQ3 (lab-to-operational gap)."),
 "2609.32691": ("read", "B", ["evaluation-validity"], EXT, "Audit of an injection benchmark harness; directly relevant to RQ2 comparability."),
 "2607.07368": ("read", "C", ["D"], RT, "Distributed attacks by coordinating agents against per-agent monitors. Primary C vs D is ambiguous: adjudication requested."),
 "2609.33102": ("read", "C", [], MIX, "Evaluation framework jointly varying attack, defence and architecture in multi-agent systems."),
 "2604.23459": ("read", "C", [], EXT, "Empirical study of how multi-agent architecture changes attack resistance and task performance."),
 "2610.05640": ("read", "C", ["B"], EXT, "Tests whether a single-agent isolation defence composes across agents."),
 "2609.00267": ("read", "C", ["B"], EXT, "Delegation/authorization gap analysis under an untrusted-model assumption."),
 "2409.07985": ("read", "D", [], RT, "Formal game model of control evaluations; formal study, eligible under protocol if assumptions are substantive."),
 "2604.03968": ("read", "D", [], RT, "Monitoring protocol evaluated in a control setting, including same-model monitor collusion."),
 "2509.14956": ("reserve", "C", ["D"], EXT, "Architecture proposal evaluated on synthetic message classification; agent-action relevance to be checked at full text. Read v2 (evaluation replaced)."),
 "2511.02997": ("read", "D", [], RT, "Control protocols evaluated against default and adaptive red-team policies."),
 # targeted title checks W2
 "2302.12173": ("read", "B", [], EXT, "Early demonstration of indirect prompt injection in LLM-integrated applications; in window (2023)."),
 "2403.02691": ("read", "B", [], EXT, "Benchmark of indirect injection in tool-integrated agents."),
 "2503.18813": ("read", "B", [], EXT, "Capability/isolation defence by design; parent work of the multi-agent composition study (2610.05640)."),
 "2503.00061": ("read", "B", [], EXT, "Adaptive attacks against published injection defences; needed for RQ2 (attacker knowledge)."),
 "2510.09023": ("reserve", "B", [], EXT, "Adaptive attacks across jailbreak and injection defences; only part concerns agents."),
 "2309.15817": ("reserve", None, [], MIX, "LM-emulated sandbox for risky agent actions under underspecified instructions; does not map cleanly to A-D: adjudication requested."),
 "2410.09024": ("reserve", None, [], "malicious user (outside current source codes)", "Measures agent compliance with harmful user requests; the user is the adversary, a case the four boundaries do not cover: adjudication requested."),
 "2504.18575": ("read", "B", [], EXT, "Web-agent injection benchmark with end-to-end attacker goals."),
 "2506.08837": ("context", "B", [], None, "Design-pattern/position paper; positioning and citation chasing, not a primary finding source."),
 "2403.04960": ("read", "B", [], EXT, "Execution-isolation architecture; isolation defence named in T03 scope."),
 "2412.04984": ("read", "D", ["A"], ENDO, "Evaluations including oversight subversion by agents given goals in context. Primary D vs A ambiguous: adjudication requested."),
 "2502.13295": ("read", "A", [], ENDO, "Agents manipulating a game environment instead of playing; specification gaming with a shell action channel."),
 "2510.20270": ("read", "A", [], ENDO, "Benchmark where passing tests requires violating the specification."),
 "2410.07283": ("read", "C", ["B"], EXT, "Self-propagating injection between agents."),
 "2402.08567": ("reserve", "C", [], EXT, "Propagating jailbreak among multimodal agents; action-channel relevance to be checked."),
 "2402.07510": ("read", "C", ["D"], MIX, "Steganographic collusion between agents and limits of monitoring."),
 "2502.14143": ("context", "C", [], None, "Technical report/taxonomy of multi-agent risks; context only."),
 "2502.14847": ("read", "C", [], EXT, "Attacks on inter-agent communication channels."),
 "2503.12188": ("read", "C", ["B"], EXT, "Control-flow hijacking in multi-agent systems leading to code execution."),
 "2312.06942": ("read", "D", [], RT, "Original control-evaluation protocol study (trusted monitoring etc.)."),
 "2506.15740": ("read", "D", [], RT, "Sabotage and monitoring benchmark; testbed for 2511.02997."),
 "2504.10374": ("read", "D", [], RT, "Resampling control protocols in a multi-step bash setting."),
 "2410.21514": ("reserve", "D", [], RT, "Sabotage capability evaluations by a developer; overlaps other D works."),
 "2512.15688": ("read", "D", [], RT, "Control setting with privileged agents; testbed for 2604.03968."),
 "1606.06565": ("context", "A", [], None, "FOUNDATIONAL EXCEPTION (2016): source of the reward-hacking/side-effect problem framing. Outside window; cite for definitions only."),
 "1908.04734": ("context", "A", [], None, "FOUNDATIONAL EXCEPTION (2019; journal version 2021 per arXiv comment): formal definition of reward tampering. Outside window; definitions only."),
 # S4
 "2410.02644": ("read", "B", [], EXT, "Agent Security Bench. Pin v4 (see Q003)."),
 "2406.13352": ("read", "B", [], EXT, "Seed benchmark. Pin v3: title and results changed after v1 (see findings)."),
 "2510.05244": ("read", "B", ["evaluation-validity"], EXT, "Questions whether current injection benchmarks are strong enough to rank defences; RQ2."),
 "2502.05174": ("reserve", "B", [], EXT, "Defence proposal."), "2412.16682": ("reserve", "B", [], EXT, "Defence proposal."),
 "2507.02735": ("reserve", "B", [], EXT, "Training-based defence."), "2505.05849": ("reserve", "B", [], EXT, "Black-box red-teaming method."),
 "2510.04885": ("reserve", "B", [], EXT, "RL-trained attacker; adaptive-attack evidence."), "2509.25926": ("reserve", "B", [], EXT, "Privilege-separation defence."),
 "2507.05630": ("reserve", "B", [], EXT, "Failure analysis of LLM-based injection detection."), "2507.15219": ("reserve", "B", [], EXT, "Defence proposal."),
 "2510.19207": ("reserve", "B", [], EXT, "Defence proposal."), "2511.20597": ("reserve", "B", [], EXT, "Browser-agent benchmark and defence."),
 "2502.08966": ("reserve", "B", [], EXT, "Information-flow style defence."), "2506.01055": ("reserve", "B", [], EXT, "Data-leak injection study."),
 "2503.16248": ("reserve", "B", [], EXT, "Memory/context manipulation of Web3 agents."), "2512.23128": ("reserve", "B", [], EXT, "Web-agent persuasion benchmark."),
 "2511.15203": ("reserve", "B", [], EXT, "Taxonomy and evaluation of defence frameworks; partly a review."), "2506.05739": ("reserve", "B", [], EXT, "Defence proposal."),
 "2510.11238": ("reserve", "B", [], EXT, "Content manipulation without injected instructions; a boundary case for category B."),
 "2504.19793": ("reserve", "B", [], EXT, "Injection targeting tool selection."),
 "2511.15759": ("exclude", None, [], None, "RAG prompt-injection benchmark; abstract shows no tool/action channel."),
 "2508.20890": ("exclude", None, [], None, "Generic prompt-injection detector; abstract shows no agent-action evaluation."),
 "2509.14285": ("exclude", None, [], None, "Direct injection through user input with an LLM filtering pipeline; no agent action channel in abstract."),
 # S5
 "2511.18397": ("read", "A", [], ENDO, "Reward hacking arising in realistic RL training and its downstream effects."),
 "2410.06491": ("reserve", "A", [], ENDO, "In-context RL variant of the seed study's environments."),
 "2503.11926": ("read", "D", ["A"], ENDO, "Monitoring of reasoning for reward hacking in agentic coding and the obfuscation risk."),
 "2407.04549": ("exclude", None, [], None, "Evaluator gaming in text self-refinement; no agent action channel."),
 **{k: ("exclude", None, [], None, RLHF) for k in "2501.19358 2509.15557 2504.15275 2401.12187 2309.10202 2412.16475 2508.04632 2508.04216 2409.20370 2508.05613 2508.17637 2510.21053 2411.04712 2506.19248 2511.11881 2312.09244 2410.21545 2507.07375 2510.18849".split()},
 # S6
 **{k: ("reserve", "C", [], EXT, r) for k, r in {
   "2505.24201": "Graph-based anomaly detection for multi-agent systems.", "2502.11127": "Topology-guided defence for multi-agent systems.",
   "2508.09230": "Defence against propagating attacks in VLM agent groups.", "2507.13038": "Injection exploiting conformity in multi-agent debate.",
   "2510.04303": "Auditing for steganographic collusion.", "2507.06850": "Agent-to-agent trust exploitation leading to system compromise.",
   "2505.04799": "Policy enforcement for multi-agent data flows.", "2512.03097": "Collusion in a healthcare multi-agent setting.",
   "2509.13597": "Delegation protocol proposal.", "2506.02859": "Attack-graph threat assessment method."}.items()},
 "2506.15253": ("reserve", "B", [], EXT, "Specification-based tool-call security evaluation."), "2512.06556": ("reserve", "B", [], EXT, "Tool-descriptor manipulation."),
 "2512.23557": ("reserve", "B", [], EXT, "Multimodal injection defence."), "2508.02736": ("reserve", "D", [], None, "System-level observability tooling."),
 "2507.13169": ("context", "B", [], None, "Position/overview paper."), "2512.08290": ("context", "B", [], None, "Systematization of knowledge; review class."),
 "2512.12921": ("context", None, [], None, "Vendor framework report; no evaluation evident in abstract."),
 "2410.15236": ("exclude", None, [], None, "Review of LLM jailbreaks; not agent-action specific."), "2508.11733": ("exclude", None, [], None, "Communication pruning for efficiency; not a security study."),
 "2511.19483": ("exclude", None, [], None, "Tool-orchestration framework; not a security study."), "2501.00055": ("exclude", None, [], None, "Jailbreak generation against chat models; no agent action channel."),
 "2512.11933": ("exclude", None, [], None, "Governance framework proposal for finance; no security evaluation in abstract."),
 # S7
 "2512.13526": ("reserve", "D", [], RT, "Asynchronous monitoring stress test."), "2510.09462": ("read", "D", ["B"], RT, "Adaptive attacks (injection against the monitor) on control protocols; RQ2 attacker-knowledge evidence."),
 "2506.05296": ("reserve", "D", [], RT, "Cost of control protocols; utility/cost evidence."),
 "2504.05259": ("context", "D", [], None, "Position paper on evaluating control measures."), "2506.13666": ("context", "B", [], None, "Position paper on MCP third-party risk."),
 "2407.16521": ("exclude", None, [], None, "Social-deduction game capability evaluation; not a security study."), "2511.10687": ("exclude", None, [], None, "Credit assignment theory for multi-agent training."),
 "2509.25885": ("exclude", None, [], None, "Embodied-agent physical safety; outside the four boundaries studied."), "2311.10776": ("exclude", None, [], None, "Chemistry agent; unrelated."),
 "2511.02794": ("exclude", None, [], None, "Multimodal reasoning diagnostics; unrelated."),
}
# non-arXiv pilot records resolved (or not) through Crossref title search
NONARXIV = {
 "P002": dict(status="context_review", doi="10.1007/s44163-026-01980-z", date="2026-08-17", venue="Discover Artificial Intelligence (Springer)", category="A",
              reason="Existing survey: positioning and citation chasing only, not a primary finding source."),
 "P011": dict(status="include_for_reading", doi="10.3390/computers15090570", date="2026-08-31", venue="Computers (MDPI)", category="B",
              reason="Replication-style evaluation of injection defences reporting security and utility; publisher page not yet opened."),
 "P017": dict(status="awaiting_full_text", doi="10.1109/sera69989.2026.11618608", date="2026-05 (day not in Crossref)", venue="IEEE/ACIS SERA 2026", category="B",
              reason="Metadata confirmed in Crossref; IEEE full text not accessed (institutional access likely required)."),
 "P019": dict(status="reserve", doi="10.3390/computation14050098", date="2026-04-25", venue="Computation (MDPI)", category="B",
              reason="Metadata confirmed in Crossref; abstract not yet read at publisher, so no screening decision beyond eligibility."),
 "P013": dict(status="metadata_unverified", reason="No exact-title record in arXiv or Crossref. Nearest Crossref item (10.70849/ijsci03052614598) has a different title and different authors from the SciSpace record; not treated as the same work. Not citable until a primary record is found."),
 "P018": dict(status="metadata_unverified", reason="No exact-title record in arXiv or Crossref (two Crossref queries). Not citable until a primary record is found."),
 "P020": dict(status="metadata_unverified", reason="No exact-title record in arXiv or Crossref. Not citable until a primary record is found."),
 "P025": dict(status="metadata_unverified", reason="No exact-title record in arXiv or Crossref; SciSpace lists the author as 'Anonymous'. Treat as unverifiable."),
}
STATUS = {"read": "include_for_reading", "reserve": "reserve", "context": "context_only", "exclude": "excluded_at_abstract"}

matrix = json.load(open("evidence/literature_matrix_v0.1_snapshot.json"))
pilot = {s["id"]: s for s in json.load(open("evidence/arxiv_api/summary.json"))}
ext = json.load(open("evidence/arxiv_api_ext/summary.json"))
idfix = {base(e["arxiv_id_latest"]): e for e in parse(open("evidence/arxiv_api_ext/W2_idcheck_01_16.xml", "rb").read())}

works, order = {}, []
def add_work(e, disc_id, search_id):
    b = base(e["arxiv_id_latest"])
    if b not in works:
        dec, cat, sec, src, why = D[b]
        first = e["first_submitted"][:10]
        venue = "; ".join(x for x in (e["journal_ref"], e["comment"]) if x and "formatting style" not in x and re.search(r"accept|proc|ICML|ICLR|ACL|NDSS|NeurIPS|Synthese|Findings", x, re.I)) or None
        works[b] = {"work_id": None, "title": e["title"], "authors": e["authors"],
            "identifiers": {"arxiv": b, "doi": e["doi"]}, "primary_url": f"https://arxiv.org/abs/{b}",
            "first_public_date": first, "version_checked": e["arxiv_id_latest"], "version_date": e["latest_version_date"][:10],
            "venue_claim": venue, "venue_claim_basis": "author-reported arXiv comment/journal-ref; not confirmed at publisher" if venue else None,
            "peer_review_status": "claimed by authors, unconfirmed" if venue else "preprint (no venue stated on arXiv)",
            "in_review_window": "2023-01-01" <= first <= TODAY, "within_evidence_cutoff": first <= TODAY,
            "discovered_by": [], "discovery_record_ids": [],
            "gate": 4, "screening_decision": STATUS[dec], "screening_basis": "title + abstract from arXiv API record", "screening_reason": why,
            "evidence_class": "review_or_context" if dec == "context" else ("primary" if dec in ("read", "reserve") else None),
            "proposed_primary_category": cat, "secondary_tags": sec, "proposed_behaviour_source": src,
            "coding_status": "provisional, from abstract only; confirm at full-text gate",
            "agent_reading_status": f"abstract only, via arXiv API record, {TODAY}; methods/results/conclusion NOT read",
            "human_reading_status": None, "full_text_read": False,
            "extraction": None}
        order.append(b)
    w = works[b]
    if search_id not in w["discovered_by"]: w["discovered_by"].append(search_id)
    w["discovery_record_ids"].append(disc_id)
    return b

out = []
for r in matrix:                                   # P001-P030
    r = dict(r); s = pilot[r["id"]]; r["work_id"] = None
    if s["exact_title_matches"]:
        e = s["exact_title_matches"][0]; b = add_work(e, r["id"], r["search_id"]); w = works[b]
        r.update(primary_url=w["primary_url"], publication_date_verified=True, first_public_date=w["first_public_date"],
                 version_checked=w["version_checked"], category=w["proposed_primary_category"], screening_reason=w["screening_reason"],
                 status=w["screening_decision"], evidence_locator=f"evidence/arxiv_api/{r['id']}.xml", _arxiv=b)
    else:
        n = NONARXIV[r["id"]]
        r.update(status=n["status"], screening_reason=n["reason"], evidence_locator=f"evidence/crossref_openalex/{r['id']}_crossref*.json")
        if "doi" in n:
            r.update(primary_url="https://doi.org/" + n["doi"], publication_date_verified=True, first_public_date=n["date"],
                     venue=n["venue"], category=n["category"], metadata_basis="Crossref exact-title match; publisher page not opened")
    out.append(r)
p6 = next(r for r in out if r["id"] == "P006")       # Q001: same arXiv identifier as P004
p6.update(status="duplicate", possible_duplicate_of="P004", screening_reason="Confirmed duplicate discovery record: resolves to the same arXiv work (2603.11337) as P004. Retained, not counted as a work.")
n = 30
def disc(e, sid, locator, note=None):
    global n; n += 1; pid = f"P{n:03d}"; b = add_work(e, pid, sid); w = works[b]
    out.append({"id": pid, "search_id": sid, "title": e["title"], "scispace_id": None, "url": w["primary_url"], "discovery_excerpt": note,
        "status": w["screening_decision"], "possible_duplicate_of": None, "primary_url": w["primary_url"], "publication_date_verified": True,
        "full_text_read": False, "category": w["proposed_primary_category"], "screening_reason": w["screening_reason"], "methods": None, "testbed": None,
        "metric_definition": None, "denominator": None, "findings": None, "limitations": None, "evidence_locator": locator,
        "work_id": None, "first_public_date": w["first_public_date"], "version_checked": w["version_checked"], "_arxiv": b})
for q in ext["searches"]:
    for e in q["entries"]: disc(e, q["search_id"], f"evidence/arxiv_api_ext/{q['search_id']}.xml")
for c in ext["title_checks"]:
    i = int(c["check_id"][-2:])
    if c["exact"]:
        e = next((x for x in c["exact"] if base(x["arxiv_id_latest"]) in D), c["exact"][0]); disc(e, "W2", f"evidence/arxiv_api_ext/W2_{i:02d}.xml")
    else:
        e = idfix[{1: "2302.12173", 16: "2402.07510"}[i]]
        disc(e, "W2", "evidence/arxiv_api_ext/W2_idcheck_01_16.xml", f"Title query returned no exact match (queried: {c['queried_title']!r}); resolved by arXiv identifier lookup.")
# first record of each work is canonical; later records of the same work are flagged as repeats
for k, b in enumerate(order, 1): works[b]["work_id"] = f"W{k:03d}"
seen = {}
for r in out:
    b = r.pop("_arxiv", None)
    if not b: continue
    r["work_id"] = works[b]["work_id"]
    if b in seen and r["status"] != "duplicate":
        r["repeat_discovery_of"] = seen[b]
    seen.setdefault(b, r["id"])
json.dump(out, open("literature_matrix.json", "w"), indent=1, ensure_ascii=False)
json.dump([works[b] for b in order], open("works.json", "w"), indent=1, ensure_ascii=False)

log = json.load(open("evidence/search_log_v0.1_snapshot.json"))
for q in ext["searches"]:
    log.append({"search_id": q["search_id"], "executed_date": TODAY, "source": "arXiv API (export.arxiv.org), sortBy=relevance", "query": q["query"],
        "retrieval_limit": q["retrieval_limit"], "returned_count": q["returned_count"], "total_database_hits": q["total_database_hits"], "status": "fulfilled",
        "notes": "Year-bounded extension for Q002 (2023-2025 submission dates). total_database_hits is the API's opensearch:totalResults for this query; only the top records by relevance were retrieved and screened. Raw response: evidence/arxiv_api_ext/%s.xml" % q["search_id"]})
log.append({"search_id": "W2", "executed_date": TODAY, "source": "arXiv API exact-title checks", "query": "26 separate ti:\"<exact title>\" queries; titles listed in tools/extend_search.py; 2 unresolved titles looked up by arXiv identifier",
    "retrieval_limit": 5, "returned_count": 26, "total_database_hits": None, "status": "fulfilled",
    "notes": "Purposive, not systematic: the 26 titles were leads recalled by the reviewing agent and confirmed at arXiv. returned_count counts one confirmed record per title. Report as 'other sources/citation leads' in the selection flow, not as database hits."})
log.append({"search_id": "V1", "executed_date": TODAY, "source": "arXiv API + Crossref API", "query": "Exact-title metadata verification of P001-P030 (tools/verify_arxiv.py; Crossref query.title for the 8 records absent from arXiv)",
    "retrieval_limit": None, "returned_count": 0, "total_database_hits": None, "status": "fulfilled",
    "notes": "Verification pass, not a discovery search; adds no records. OpenAlex returned HTTP 429 for all 8 queries and contributed nothing."})
json.dump(log, open("search_log.json", "w"), indent=1, ensure_ascii=False)

# BibTeX for works not excluded (candidate library; final list depends on full-text gate)
def key(w): return re.sub(r"[^A-Za-z]", "", w["authors"][0].split()[-1]) + w["first_public_date"][:4] + re.sub(r"[^A-Za-z]", "", w["title"].split()[0].split(":")[0])
bib = ["%% Candidate reference library generated from arXiv API metadata on %s." % TODAY,
       "% Venue notes are author-reported and unconfirmed; replace @misc with the published entry after checking the publisher.", ""]
for b in order:
    w = works[b]
    if w["screening_decision"] == "excluded_at_abstract": continue
    bib.append("@misc{%s,\n  author = {%s},\n  title = {{%s}},\n  year = {%s},\n  eprint = {%s},\n  archivePrefix = {arXiv},\n  url = {%s},\n  note = {%s; version checked %s (%s); queue: %s%s}\n}\n" % (
        key(w), " and ".join(w["authors"]), w["title"], w["first_public_date"][:4], b, w["primary_url"], w["work_id"], w["version_checked"], w["version_date"],
        w["screening_decision"], ("; author-reported venue: " + w["venue_claim"]) if w["venue_claim"] else ""))
open("references_candidates.bib", "w").write("\n".join(bib))
