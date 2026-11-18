# Briefing for agents joining this project

Updated 17 November 2026 for the author-edited LaTeX v0.7 release. The user has authorized integration of the outstanding PRs. Human academic checks remain separate from repository merging.

## Canonical v0.7 source

Edit `paper/latex_v0.7/` and follow its README. `MANUSCRIPT.md`, `paper/content.py` and `tools/build_paper.py` retain v0.6 source snapshots; do not use them to overwrite the user's v0.7 edits. The new workflow compiles XeLaTeX and records source, page, corpus, questionnaire and numeric-string audits. Review `evidence/audit_v07_conversion.json` for conversion parity and the latest handoff for visual QA.

Human reading reported in the edited draft: Parivesh Singh 7 works; Vaibhav Gaur 3. Work IDs and overlap are unknown. Keep these aggregate reports separate from AI-assisted extraction of 35 included works and 7 read-but-not-included works. Do not change per-work human reading flags without the corresponding work IDs. Future intended reading is not completed reading.

Supervisor: Dr. Abhishek Pandey (name corrected by the user on 18 Nov 2026); user-confirmed email `abhishek.pandey@iilm.edu`. Assessment marks intentionally blank. Declaration/signatures and final human source/originality checks remain pending. Questionnaire must not be distributed without supervisor approval.

## Prior v0.6 briefing (historical snapshot)

# Briefing for agents joining this project

Updated 17 November 2026 by the ChatGPT coordinator after the v0.6 rebuild on draft PR 4. Read this, then `MESSAGE_BOARD.md` (version 0.4), then the latest file in `handoffs/` and `evidence/second_reader/`. `BASE_PROMPT.md` and `REVIEW_PROTOCOL.md` still govern how evidence is handled.

## What the project is

A literature survey for a B.Tech course at IILM University, written by the student (Paarv) in the professor's template: *Security Failures in Autonomous AI Agents: A Survey Motivated by the OpenAI–Hugging Face Incident*. You are an assistant, not an author. Do not claim credentials, do not state that the student read anything, and do not sign or fill declarations.

## Where things stand

| Item | State |
|---|---|
| Paper | Draft v0.6: `paper/AgentSecuritySurvey_draft_v0.6.docx` / `.pdf`, `MANUSCRIPT.md`. 12-page paper block (15 PDF pages including cover and annexure), 3 figures, 11 tables, 40 references |
| Corpus | 234 records → 212 works screened → 43 queued → 35 included (A 10, B 9, C 8, D 8), 7 read but not included, 1 not read |
| Reading | Initial extraction by one AI reviewer from stated sections at pinned arXiv versions. AI second-reader batch 1 checked four high-impact work claims, F3, F6 and the OpenAI 198/898/93 figures. **Human reading confirmed: 0; human second-reader checks: 0** |
| Incident | 35-entry claim ledger from Hugging Face (16 and 27 Jul 2026), OpenAI (26 Aug 2026) and METR (26 Aug 2026); OpenAI technical report read in part. The accounts are not independent |
| Questionnaire | `survey/`, v0.2, 17 items. Not administered. No responses exist |
| Pull request | Draft PR 4 on branch `chatgpt/t09-second-reader-batch1`; do not merge until the coordinator accepts the remaining human gates |

## Files that matter

| File | What it is |
|---|---|
| `works.json` | One record per distinct work (212): identifiers, pinned version, screening decision, category, reading status, canonical discovery record, published record if found. Every selection count is a count of works by `screening_decision` |
| `literature_matrix.json` | One record per discovery hit (234). `work_id` links a record to its work; `repeat_of_record` links a later record of the same work to the canonical record (record IDs only). Unverified records have no work |
| `extraction_matrix.json` | Full-text extraction for the 35 included works, with sections read |
| `incident_claim_ledger.json` | Dated, attributed incident claims, disagreements and visibility limits |
| `search_log.json` | Every search run, and those not run, with reasons |
| `paper/extraction_data.py` | Source of the extraction records and incident ledger |
| `paper/content.py` | Source of all manuscript text and tables. Later blocks override earlier ones; the last assignment wins |
| `paper/counts.json` | Every count used in the paper; generated, never typed |
| `references.bib` | The 40 references in citation order |
| `survey/build_questionnaire.py` | Single source for the questionnaire, its CSV, codebook and empty responses template |

## How to rebuild and check

```bash
python3 tools/build_t02.py && python3 tools/build_paper.py
```

```bash
python3 tools/audit_paper.py
```

```bash
python3 tools/check_corpus.py
```

```bash
python3 survey/build_questionnaire.py && python3 tools/check_questionnaire.py
```

GitHub Actions (`.github/workflows/checks.yml`) runs the corpus audit, the structural manuscript audit (`tools/audit_paper.py --structural`) and the questionnaire checks on every pull request. `.github/workflows/build-paper-v06.yml` rebuilds the DOCX/PDF, renders every page and records the page-boundary and numeric-source audits when paper sources change.

The audit checks the selection arithmetic, table and figure structure, and that every number in a citing sentence appears in the saved text of a cited source. Saved full texts live in `evidence/fulltext/` and `evidence/incident/` and are not committed (copyright); without them the numeric check reports the sources as unavailable. Re-fetch at the versions in `works.json` (arXiv HTML) if you need them. PDF conversion uses LibreOffice (`soffice --headless --convert-to pdf`); figures need matplotlib.

## Rules that have already caught errors

1. **Counts come from the ledgers.** Change the data, rebuild, and let the text follow. Never type a count into `content.py`.
2. **A number may be quoted only if it is in the cited source's text**, and only with the meaning the source gives it. The audit checks the first half; you must check the second by reading. One "rose from X to Y" in an earlier draft was really a comparison with a baseline model.
3. **Never pool or rank rates across studies.** Exploit rates, attack success rates and control "safety" have different denominators and different sources of behaviour.
4. **Attribute incident statements** to a named report and date. Do not write what "happened"; write what a report says. Do not treat the three accounts as independent confirmation.
5. **Search summaries and AI-generated text are not evidence.** Web search was used only to find URLs.
6. **The questionnaire has no data.** Do not enter, simulate or estimate responses, and do not describe results. `survey/responses_template.csv` must stay header-only until real exports exist.
7. **Limits bind:** 12 pages for the paper block, 25–40 references (currently 40, so adding a source means removing one), abstract 150–250 words, no "comprehensive", "exhaustive" or "best".
8. **Board discipline:** append a message with a unique ID; do not rewrite earlier messages. Work on a branch and push; do not merge.

## What you can usefully do next

| Task | Notes |
|---|---|
| T09 second-reader check | Continue with claims not covered by `evidence/second_reader/t09_batch1_20261117.md`, `t09_f6_utility_20261117.md` and `t09_openai_numbers_20261117.md`. F3 and F6 are checked; F6 is 15/35 (A 2, B 5, C 2, D 6). Do not count runtime/cost alone as legitimate-task utility |
| T13 incident sources | The Black Hat talk was not accessed and OpenAI's technical report was read only in part (ledger I30–I35). Add any contradicting claim to the ledger before touching Section V.D |
| T10 native database searches | Needs institute access or a human. Log every query, date and hit count; do not relabel a web search as a database search |
| Q010 | Consolidate `paper/content.py` so each variable is defined once; rebuild and confirm the audit output is unchanged |
| T14 | P011 (MDPI) needs a browser |

Humans only: T08 (reading), T11 (supervisor approval and distribution of the questionnaire), and the remaining T12 items (acknowledgment, contribution allocation, signatures, final filename and cover fields). Author/course/supervisor metadata is already filled.

## Environment notes

The cloud environment named `autonomous-agent-security-survey` allows: arxiv.org, export.arxiv.org, api.crossref.org, api.openalex.org, openreview.net, doi.org, huggingface.co, openai.com, metr.org, en.wikipedia.org, ieeexplore.ieee.org, dl.acm.org, link.springer.com, www.mdpi.com. In practice openai.com and www.mdpi.com return HTTP 403 to automated requests, OpenAlex rate-limited every call, and Google Scholar, Reddit and YouTube could not be added. Do not script requests against a publisher's internal search endpoints.
