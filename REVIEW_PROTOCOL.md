# Review protocol version 0.1

Status: prospective protocol for screening after a logged pilot search. Not preregistered. Any changes will be dated and justified; do not describe this as fixed before earlier exploratory research.

## Scope and questions

Study security-relevant failures and defenses in language-model agents with action channels: tool execution, file modification, environment access or inter-agent communication. Address objective integrity, authorization, coordination and oversight. The three review questions are in BASE_PROMPT.md. Do not equate an externally attacked agent with an agent exploiting its own objective.

Window: first publication from 1 January 2023 to 16 November 2026. Earlier foundational works require an explicit exception. Record first-publication date and the date of the version actually read. Recent-year counts use unique works; the inclusion window is narrower than the professor's five-year condition.

## Corpus design

Maintain three evidence classes: empirical or formal primary research for the core comparison; reviews for positioning and citation chasing; incident/official reports for the motivating case. Report their counts separately. Aim for at least 25 relevant reviewed works overall without inflating the count using versions or multiple summaries of the same incident. Prefer most of the corpus to be primary research. Whether to include a formal study without experiments depends on whether it provides substantive analysis and assumptions relevant to the review questions.

Include English full-text work with a defined security mechanism and an evaluation, formal analysis or documented incident evidence. Exclude generic chatbot safety with no agent-action relevance, editorials without methods/evidence, one-page abstracts, duplicates, unverifiable references and works beyond cutoff. Access failures remain awaiting_full_text until resolved; do not pretend the paper was read. Retain existing surveys as context, not independent experiments.

## Search procedure

S1–S3 in search_log.json are executed SciSpace natural-language queries. They returned ten records each. The provider did not supply total database hits. The log records null for that field. search_results_raw.json preserves the full returned records. Earlier searches in the conversation are exploratory and outside this pilot's counts.

Further work should use exact-title and year-bounded queries, publisher/arXiv retrieval, and backward/forward citation chasing. Do not label a web domain-filtered search a native IEEE/ACM database search. Add a log row for each real query; never populate the professor's example database rows unless those searches were performed.

Targeted web check W1, 16 November 2026: queries `site.arxiv.org "AgentDojo"`, `site.arxiv.org "Agent Security Bench"`, and `site.arxiv.org "Sycophancy to Subterfuge"`. These were metadata/primary-source checks, not an exhaustively enumerated retrieval batch. Primary pages opened: https://arxiv.org/html/2406.10162v1 and https://arxiv.org/html/2406.13352v1. Initial abstract/introduction excerpts were inspected; this is not a full-text reading claim. These checks do not alter S1–S3 counts.

## Selection and reading gates

1. Discovered: a search record exists.
2. Metadata verified: primary identifier, date and version confirmed.
3. Deduplicated: work identity confirmed; excluded duplicates retain parent IDs.
4. Abstract screened: explicit include-for-reading or exclusion reason.
5. Sections read: abstract, methods and conclusion accessed and recorded; result-bearing pages checked for numerical claims.
6. Extracted: matrix complete for required fields, with missing values explicit.
7. Reviewed: a second reader checks central claims and selection reason.
8. Included: coordinator accepts evidence; human reading completion still recorded separately.

The current matrix is at gate 1. Its null extraction fields are intentional. The possible duplicate is not yet a confirmed exclusion. No selection-flow final number can be inferred from 29 normalized titles.

## Extraction and quantitative analysis

One discovery row per returned record; later one canonical work record per intellectual work with links to versions and queries. For quantitative synthesis use one result record per study × model × task × attack/defense configuration, not one ambiguous percentage per paper. Record numerator, denominator, metric definition, attack budget, task horizon, tool permissions, model date/version, benign utility, cost and uncertainty. Add study_id so related results are not treated as independent samples.

Descriptive outputs will include included-work counts by year and primary category, coverage of benchmarks and availability of reproducibility artifacts. Their denominators must be stated. Missingness is a result about reporting, not evidence a study did not perform an analysis. A year chart describes this selected corpus, not the size of the entire field. Do not draw it from the pilot's ranked search results.

Use grouped comparisons for compatible setups and narrative contrasts otherwise. Do not create a universal model-safety ranking or pooled attack success rate from incompatible studies. Preserve uncertainty and failed replications. Suggested quality fields are verification status, stated threat model, adaptive-attacker test, utility measurement, execution-log availability, replication resources and limitations; do not invent a numerical quality score.

## Figures and tables planned

Figure 1 selection flow from actual screening ledger; Figure 2 taxonomy with representative included studies; Figure 3 included works per year/category. Tables: executed searches, criteria, taxonomy mapping, category comparisons, master comparison, benchmark/metric caveats and evidence-backed gaps. Final numbering follows the professor's format. Figures and results remain pending until the input corpus supports them.

## Integrity and release

Two researchers reviewing claims is a proposed process, not a completed independent review. Track actual reviewer identities, disagreement and resolution. Do not claim exhaustive coverage, preregistration, experimental causality, verified incident logs, or an independently reproduced breach. Keep prior case-study arithmetic separate from literature statistics. Submit a truthful AI-use statement and have each human author confirm their own paper-reading record.

## Amendment log

**2026-11-16, proposed by claude-t01 (message claude-t01-20261116-001), pending coordinator acceptance.** After the pilot, four year-bounded arXiv API searches (S4-S7, submission dates 2023-2025, top 25 by relevance) and 26 targeted exact-title checks (W2) were added to address Q002. These were designed after seeing the pilot results and are not part of a predetermined protocol. `works.json` was introduced as the one-record-per-work ledger foreseen under "Extraction". Screening statuses in use: include_for_reading, reserve, context_only/context_review, excluded_at_abstract, duplicate, awaiting_full_text, metadata_unverified. "reserve" is new: eligible on abstract, read only if coverage or capacity requires.
