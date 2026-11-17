> Superseded by `MANUSCRIPT.md` (draft v0.5). Kept unchanged below as the v0.1 starting point.

# Security Failures in Autonomous AI Agents

## A Survey Motivated by the OpenAI–Hugging Face Incident

Working manuscript v0.1 | 16 November 2026

Status: research framing and methodological starter. This is not the final 3,500–5,000-word paper. Inclusion counts, abstract findings, figures and comparative results are intentionally pending. Use stable source labels during drafting; convert to numbered IEEE citations after integration.

## I Introduction

Autonomous language-model agents combine generated decisions with tools that can change an external environment. Their evaluation must therefore distinguish successful task completion from authorized task completion. A high score is insufficient evidence of either secure execution or a valid evaluation process. The relevant research spans several settings: a model exploiting a scoring objective, an attacker redirecting an otherwise legitimate agent, and a supervisor failing to detect an unwanted action. These settings share an interest in control but make different assumptions about where the harmful behavior originates.

Two examples illustrate why the distinction matters. Denison et al. investigate generalization from simpler specification gaming to reward tampering under a constructed training curriculum [SEED-A]. AgentDojo studies tool-using agents interacting with untrusted data, where malicious content can redirect behavior [SEED-B]. The first concerns a route from optimization to unintended behavior; the second concerns an adversarial input channel. A comparison must retain that difference rather than placing both results on an undifferentiated “agent risk” scale.

The OpenAI–Hugging Face incident supplies an operational motivation for asking how these research settings connect to unauthorized activity beyond a benchmark. Its documentation will be analyzed in a separate case-evidence ledger before detailed claims are integrated. The incident will illustrate the review's categories without being treated as a controlled experiment or as proof that all deployed agents exhibit the same behavior.

### Review questions

RQ1: Which mechanisms allow autonomous AI agents to violate intended objectives or authorization boundaries?

RQ2: How are failures and defenses evaluated, and which reported outcomes can validly be compared?

RQ3: What limitations remain when applying laboratory findings to operational incidents?

### Intended contributions

The review will provide an explicit search and selection record; a taxonomy based on the primary boundary studied; a comparison of methods and evaluation assumptions; and evidence-supported research gaps. These are intended outputs, not completed findings. The final abstract will state only the corpus and conclusions that the completed matrix supports.

## II Review Methodology

A pilot search was executed on SciSpace on 16 November 2026 using three queries covering evaluation integrity, input/tool authorization, and multi-agent/control research. Each query returned ten records, yielding 30 discovery records. Normalized-title comparison identified 29 distinct titles and one possible duplicate pair. The provider did not report total database hits. These numbers describe retrieval only; final work-level deduplication and inclusion decisions have not been completed.

The review protocol sets a provisional 2023–16 November 2026 window, with justified foundational exceptions. Primary empirical or formal studies will supply the principal comparison. Existing reviews will support positioning and citation chasing, while official incident reports will support the motivating example. Each accepted work will have primary metadata verification, recorded reading of abstract/methods/conclusion, and evidence locators for extracted claims. Changes to this protocol will be dated rather than retrospectively presented as predetermined.

Outcomes will be compared only when their definitions and experimental conditions permit it. The extraction schema records attacker knowledge, model/version, task environment, permissions, budget, metric and denominator. It also records legitimate-task utility so that a defense is not evaluated solely by its ability to stop activity. Corpus trends will describe selected works, not all publications in the field.

## III Provisional Taxonomy

| Primary category | Boundary under study | Example questions |
|---|---|---|
| A Objective and evaluation integrity | Intended goal versus measured objective | Can a score be increased without completing the intended task? |
| B Input and tool authorization | Untrusted content versus executable authority | Can external data redirect privileged tool use? |
| C Inter-agent trust and communication | Information and authority passed between agents | Can coordination spread an unsafe action or bypass run isolation? |
| D Oversight and control integrity | Agent behavior versus supervisory enforcement | Can unwanted behavior evade or manipulate monitoring? |

Each work will receive one primary category according to its principal evaluated mechanism, with secondary tags retained. The source of unsafe behavior—external attack, endogenous optimization, prompted red team, or mixed/unclear—will be coded separately. This avoids confusing who initiates a behavior with which system boundary it crosses. The taxonomy will be revised if pilot screening exposes persistent ambiguity.

## IV Literature Review — initial comparison note

SEED-A and SEED-B should not be compared through their headline success rates. Their environments, failure definitions and intervention points differ. A useful comparison instead asks which assumption is violated, which action becomes possible, and where a defense can enforce the intended boundary. Full methods/results extraction is pending, so this note makes no numerical cross-study comparison.

## V Comparative Analysis and Discussion

Pending: category comparisons, master matrix, benchmark caveats and corpus trend. The earlier incident action-count arithmetic must not be substituted for the required literature comparison.

## VI Research Gaps and Open Challenges

Candidate questions for testing against the corpus: Do evaluations test adaptive adversaries? Do they preserve legitimate utility? Do isolated-run guarantees survive communication? Are outcomes verified independently of the agent's narrative? These are screening questions, not established gaps. Each final gap requires explicit supporting studies and counterexamples.

## VII Future Directions

Pending: three to five directions linked to accepted gaps. Avoid generic recommendations before the evidence is synthesized.

## VIII Conclusion

Pending completion of the included corpus and answers to RQ1–RQ3.

## Working source register

SEED-A: C. Denison et al., Sycophancy to Subterfuge: Investigating Reward-Tampering in Large Language Models, arXiv:2406.10162v1, 2024. Initial abstract/introduction inspected; full methods/conclusion extraction pending. https://arxiv.org/html/2406.10162v1

SEED-B: E. Debenedetti et al., AgentDojo: A Dynamic Environment to Evaluate Attacks and Defenses for LLM Agents, arXiv:2406.13352v1, 2024. Initial abstract/introduction inspected; final publication/version reconciliation and methods extraction pending. https://arxiv.org/html/2406.13352v1

The stable source labels are drafting aids, not final citation numbers. Discovery excerpts and AI-generated summaries are not bibliography entries.
