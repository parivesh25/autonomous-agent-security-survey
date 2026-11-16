#!/usr/bin/env python3
"""T01 extension: year-bounded arXiv API searches (S4-S7) and targeted
exact-title checks (W2). Saves raw Atom receipts and a parsed summary.
Usage: python3 tools/extend_search.py evidence/arxiv_api_ext
"""
import json, re, sys, time, urllib.parse, urllib.request
import xml.etree.ElementTree as ET
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from verify_arxiv import parse, norm

WIN = "submittedDate:[202301010000 TO 202512312359]"
SEARCHES = {
 "S4": f'abs:"prompt injection" AND abs:agent AND (abs:benchmark OR abs:defense) AND {WIN}',
 "S5": f'(abs:"reward hacking" OR abs:"specification gaming" OR abs:"reward tampering") AND (abs:"language model" OR abs:LLM) AND {WIN}',
 "S6": f'abs:"multi-agent" AND (abs:"prompt injection" OR abs:collusion OR abs:infection) AND (abs:LLM OR abs:"language model") AND {WIN}',
 "S7": f'(abs:"AI control" OR abs:"trusted monitoring" OR abs:sabotage) AND abs:agent AND (abs:LLM OR abs:"language model") AND {WIN}',
}
LIMIT = 25
TITLES = [  # reviewer-recalled leads; each must be confirmed by the API response
 "Not what you've signed up for: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection",
 "InjecAgent: Benchmarking Indirect Prompt Injections in Tool-Integrated Large Language Model Agents",
 "Defeating Prompt Injections by Design",
 "Adaptive Attacks Break Defenses Against Indirect Prompt Injection Attacks on LLM Agents",
 "The Attacker Moves Second: Stronger Adaptive Attacks Bypass Defenses Against LLM Jailbreaks and Prompt Injections",
 "Identifying the Risks of LM Agents with an LM-Emulated Sandbox",
 "AgentHarm: A Benchmark for Measuring Harmfulness of LLM Agents",
 "WASP: Benchmarking Web Agent Security Against Prompt Injection Attacks",
 "Design Patterns for Securing LLM Agents against Prompt Injections",
 "IsolateGPT: An Execution Isolation Architecture for LLM-Based Agentic Systems",
 "Frontier Models are Capable of In-context Scheming",
 "Demonstrating specification gaming in reasoning models",
 "ImpossibleBench: Measuring LLMs' Propensity of Exploiting Test Cases",
 "Prompt Infection: LLM-to-LLM Prompt Injection within Multi-Agent Systems",
 "Agent Smith: A Single Image Can Jailbreak One Million Multimodal LLM Agents Exponentially Fast",
 "Secret Collusion among Generative AI Agents",
 "Multi-Agent Risks from Advanced AI",
 "Red-Teaming LLM Multi-Agent Systems via Communication Attacks",
 "Multi-Agent Systems Execute Arbitrary Malicious Code",
 "AI Control: Improving Safety Despite Intentional Subversion",
 "SHADE-Arena: Evaluating Sabotage and Monitoring in LLM Agents",
 "Ctrl-Z: Controlling AI Agents via Resampling",
 "Sabotage Evaluations for Frontier Models",
 "BashArena: A Control Setting for Highly Privileged AI Agents",
 "Concrete Problems in AI Safety",
 "Reward Tampering Problems and Solutions in Reinforcement Learning: A Causal Influence Diagram Perspective",
]

def get(q, n, sort=None):
    p = {"search_query": q, "max_results": n}
    if sort: p.update(sortBy=sort, sortOrder="descending")
    url = "https://export.arxiv.org/api/query?" + urllib.parse.urlencode(p)
    for i in range(4):
        try:
            with urllib.request.urlopen(url, timeout=90) as r: return url, r.read()
        except Exception as e:
            err = e; time.sleep(6 * (i + 1))
    raise err

out = sys.argv[1]; summary = {"searches": [], "title_checks": []}
for sid, q in SEARCHES.items():
    url, raw = get(q, LIMIT, "relevance"); open(f"{out}/{sid}.xml", "wb").write(raw)
    total = int(ET.fromstring(raw).findtext("{http://a9.com/-/spec/opensearch/1.1/}totalResults"))
    ents = parse(raw)
    summary["searches"].append({"search_id": sid, "query": q, "url": url, "retrieval_limit": LIMIT,
                                "returned_count": len(ents), "total_database_hits": total, "entries": ents})
    print(sid, total, len(ents), flush=True); time.sleep(3.2)
for i, t in enumerate(TITLES, 1):
    q = 'ti:"%s"' % " ".join(re.sub(r"[^A-Za-z0-9 ]", " ", t).split())
    url, raw = get(q, 5); open(f"{out}/W2_{i:02d}.xml", "wb").write(raw)
    ents = parse(raw); exact = [e for e in ents if norm(e["title"]) == norm(t)]
    summary["title_checks"].append({"check_id": f"W2-{i:02d}", "queried_title": t, "url": url,
                                    "returned": len(ents), "exact": exact, "others": ents if not exact else []})
    print(f"W2-{i:02d}", len(ents), [e["arxiv_id_latest"] for e in exact], flush=True); time.sleep(3.2)
json.dump(summary, open(f"{out}/summary.json", "w"), indent=1, ensure_ascii=False)
