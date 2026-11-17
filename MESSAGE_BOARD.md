# Research coordination message board

Project AGENT-SEC-SURVEY | Version 0.3 | Updated 17 November 2026

**State:** draft v0.5 of the paper exists; the corpus contains 212 distinct screened works, 35 of which are included. The incident ledger contains 35 entries. All paper reading so far is by an AI assistant; human reading, second-reader checks and administrative details remain outstanding. The canonical copy of this board is this file in the shared repository `parivesh25/autonomous-agent-security-survey`. New agents: read `AGENT_BRIEFING.md` first.

Version 0.2 was written by claude-t02 on Paarv's instruction of 17 November 2026 to close open items. Version 0.3 synchronizes the accepted PR 2 state after independent reconciliation. Entries below marked (17 Nov) were added then; Paarv, as coordinator, may reverse any of them. Messages remain append-only.

## Decisions

| ID | Decision | Basis |
|---|---|---|
| D001 | Literature survey; no participant survey | Professor's template. **Superseded in part by D007.** |
| D002 | Incident is a motivating example, not the entire corpus | Need comparison across at least 25 works |
| D003 | Review period 2023–16 Nov 2026; older exceptions documented | No pre-2023 work is cited in v0.5 |
| D004 | Do not pool incomparable attack-success rates | Different tasks, threat models and denominators |
| D005 | Separate agent-assisted reading from student reading | Template's declaration and viva requirements |
| D006 | Keep stable paper IDs until final reference numbering | Prevent citation collisions across agents |
| D007 | A short practitioner questionnaire is kept as a side instrument with a growth plan. The paper stays a literature survey and reports no questionnaire results until a real round is collected (17 Nov) | Paarv's instruction, 17 Nov 2026 |
| D008 | Pinned versions: AgentDojo arXiv v3, Sycophancy to Subterfuge v3, Agent Security Bench v4 (17 Nov) | Titles/results changed between versions (handoff claude-t01-20261116-001) |
| D009 | Category rulings: multi-agent AI control (W013) = C, secondary D; in-context scheming (W115) = D, secondary A; "Architecture Matters" (W015) = C with source "malicious user"; ToolEmu and AgentHarm fall outside A–D and are not included (17 Nov) | Principal boundary tested; closes Q004 |
| D010 | At most 40 references. Works read but repeating a mechanism or test bed already represented are recorded as read, not included (17 Nov) | Template limit of 25–40 references |
| D011 | Incident statements are attributed to a named report and date; the three accounts are treated as not independent (17 Nov) | METR worked from operator-supplied data and scope |

## Task queue

| Task | Scope | Status |
|---|---|---|
| T01 | Search, metadata verification, screening | DONE by AI (PR 1 merged). Native IEEE Xplore / ACM / SpringerLink / Scholar searches NOT run: see T10 |
| T02–T04 | Full-text reading and extraction, categories A–D | DONE by AI for 35 included works and 7 read-not-included. **Human reading: 0 works. See T08** |
| T05 | Incident claim ledger | DONE by AI: 35 entries. OpenAI's technical report was read in part; the Black Hat talk was not accessed: see T13 |
| T06 | Comparison tables, figures, general findings | DONE by AI (computed from the ledgers) |
| T07 | Manuscript in the professor's template | DRAFT v0.5 (DOCX, PDF, Markdown). Placeholders remain: see T12 |
| T08 | Each team member reads the works in their categories and records it in `works.json` (`human_reading_status`) | OPEN: humans only |
| T09 | Second reader checks quoted numbers and the hand-coded counts (F3, F6) against pinned versions | IN PROGRESS: independent AI batch 1 checked F3 and four high-impact claims; one protocol-comparison correction is required. Human confirmation remains open |
| T10 | Native database searches with institute access, logged in `search_log.json`; or keep Table I as is | OPEN |
| T11 | Questionnaire: supervisor approval, form build from `survey/questionnaire.csv`, pilot with 5–8 people | OPEN: must not be distributed before approval |
| T12 | Names, enrolment numbers, course details, supervisor, acknowledgment, contribution table, AI-use statement, file name | OPEN: humans only |
| T13 | Watch the Black Hat talk and read OpenAI's technical report; add contradicting claims to the incident ledger | PARTLY DONE: technical report read in part, no contradiction with the operator's post found on statements the paper uses (ledger I30–I35). Black Hat talk still not accessed; a cover-to-cover read of the report is still owed |
| T14 | Obtain P011 (MDPI) through a browser; decide whether to read it | OPEN, low priority |

## Known issues

| Issue | Status |
|---|---|
| Q001 P004/P006 duplicate | CLOSED: same work (arXiv:2603.11337) |
| Q002 Pilot favoured 2026 | CLOSED: year-bounded searches added; included works span 2023–2026 |
| Q003 ASB version | CLOSED by D008 |
| Q004 Taxonomy overlap | CLOSED by D009 |
| Q005 No shared repository | CLOSED: repository exists |
| Q006 Inclusion and reading counts | PARTLY OPEN: 35 works included on AI reading; human reading count is 0 |
| Q007 Table VIII has 8 rows; template suggests 10–15 | CLOSED in v0.5: 12 rows, three per category, within 12 pages |
| Q008 Paper cites arXiv versions; published records found in Crossref for 10 of 35 works (`works.json`, `references.bib`) | DECIDED (PR 2 review): evidence stays tied to the arXiv version read; the DOI of a published record is added to the reference without implying the published text was read |
| Q009 Prose is about 3,900 words; with tables about 5,600 | OPEN: depends on how the professor counts |
| Q010 `content.py` holds v0.2 text followed by later overrides | OPEN, cosmetic: consolidate before further editing |

## Append-only messages

### COORD-20261116-001

- Agent: ChatGPT coordinator; task: project setup; status: completed for v0.1.
- Created brief, base prompt, protocol, board, initial manuscript and discovery records.
- Executed S1–S3, 10 returned records each: 30 records and 29 normalized titles.
- Flagged P004/P006 as a possible duplicate; did not declare final deduplication.
- No new-batch paper is marked fully read or included. Earlier exploratory work remains contextual, outside these counts.
- Next action: claim T01–T04 and return evidence-located matrix patches.

### Message template

Copy the handoff block from BASE_PROMPT.md. Include the board version read and do not edit prior messages. For conflicting claims, cite both sources and versions, identify the exact disagreement, and propose a resolution or leave it unresolved. Only the coordinator changes accepted decisions and increments the board version after merging.

### claude-t01-20261116-001

- Agent: claude-t01 (AI assistant); task: T01, self-claimed because the assignment block was blank; coordinator acknowledgement pending. Board version read: 0.1. Status: ready_for_review.
- Workspace: branch `claude/lucid-bardeen-z2si07` of the shared repository; not merged. This message is the only edit to this board; decisions, tasks, issues and version are unchanged.
- Verified P001-P030 at arXiv/Crossref: 22 records map to 21 arXiv works, 4 to Crossref DOIs, 4 are unverifiable (P013, P018, P020, P025).
- Q001: P004 and P006 are the same work (arXiv:2603.11337). Proposed resolution: P006 = duplicate.
- Q002: ran S4-S7 (arXiv API, 2023-2025) and W2 (26 targeted title checks). Ledger now has 144 discovery records and 130 works with verified metadata.
- Q003: propose pinning ASB at arXiv v4 (2025-05-30). Also propose pinning AgentDojo v3 (title and results changed after v1) and Sycophancy to Subterfuge v3.
- Q004: adjudication requested for W013 (P021), W115 (in-context scheming), W110 (ToolEmu), W111 (AgentHarm).
- Q005: a shared repository now exists; coordinator to update.
- Q006: unchanged. Abstract screening gives a 43-work reading queue (A 11, B 13, C 9, D 10). Works read in full: 0. Works included: 0.
- Full handoff: `handoffs/claude-t01-20261116-001.md`.
- Next action: coordinator review; T02-T04 full-text reading at pinned versions; T05 incident ledger.

### claude-t02-20261116-001

- Agent: claude-t02 (AI assistant); tasks: T02, extended by Paarv to T03-T07. Board version read: 0.1 plus claude-t01-20261116-001. Status: ready_for_review.
- Read 32 works at pinned arXiv versions (A 9, B 9, C 7, D 7); extraction in `extraction_matrix.json` with sections read per work.
- T05: `incident_claim_ledger.json` built from Hugging Face's posts of 16 and 27 July 2026. OpenAI's report could not be retrieved and is not cited.
- Searches: nine publisher-filtered Crossref queries logged (D1-D9). Native IEEE Xplore, ACM DL, SpringerLink, Google Scholar and Reddit were NOT searched; reasons in `search_log.json` X1-X2.
- Draft v0.2 of the paper: `MANUSCRIPT.md` and `paper/AgentSecuritySurvey_draft_v0.2.docx` / `.pdf`.
- Human reading confirmed: 0 works. Second-reader checks: 0. The declaration must not be signed yet.
- Full handoff: `handoffs/claude-t02-20261116-001.md`.

### claude-t02-20261116-002

- Agent: claude-t02 (AI assistant). Status: ready_for_review. Supersedes the counts and incident reading in claude-t02-20261116-001.
- Read OpenAI's report of 26 Aug 2026 (saved copy supplied by Paarv) and METR's investigation of the same date; incident ledger now has 29 entries. The three accounts are recorded as not independent.
- Second reading batch: 3 more works included (35 total: A 10, B 9, C 8, D 8), 6 read and set aside, 2 not read.
- Draft v0.3: `paper/AgentSecuritySurvey_draft_v0.3.docx` / `.pdf`, `MANUSCRIPT.md`. 40 references.
- `tools/audit_paper.py` added: arithmetic and structure checks pass; 102 of 102 cited numbers found in the cited sources.
- Not accessed: Black Hat talk video, OpenAI's full technical report, P011, IsolateGPT.
- Human reading confirmed: 0 works. Second-reader checks: 0.
- Full handoff: `handoffs/claude-t02-20261116-002.md`.

### claude-t02-20261117-003

- Agent: claude-t02 (AI assistant). Status: ready_for_review.
- Added Section V.E and Table X (six general findings, each with support and qualification). Gaps are now Table XI. Draft v0.4 in `paper/`.
- Added `survey/`: a 17-item practitioner questionnaire (16 closed items), not administered, no responses. Mentioned in one sentence under Future Directions only.
- Proposed decision for the coordinator to record: "D007: A short practitioner questionnaire is kept as a side instrument with a growth plan; it supersedes D001 in that respect. The paper remains a literature survey (D002) and reports no questionnaire results until a real round is collected." The decisions table itself is not edited by this message.
- The questionnaire must not be distributed before supervisor approval.
- Full handoff: `handoffs/claude-t02-20261117-003.md`.

### claude-t02-20261117-004

- Agent: claude-t02 (AI assistant). Status: ready_for_review. Board raised to version 0.2 on Paarv's instruction to close open items; decisions D007–D011, tasks T08–T14 and issue statuses were written in this pass.
- Read the last fetched paper (IsolateGPT): recorded as read, not included. Queue is now 35 included + 7 read-not-included + 1 not read (P011).
- Published-version lookup: Crossref records found for 10 of 35 included works; stored in `works.json`. The paper still cites the arXiv versions read.
- `references.bib` now holds the paper's 40 references in citation order; the T01 candidate list moved to `evidence/`.
- Questionnaire v0.2 exported as `survey/questionnaire.csv`, with `codebook.csv` and a header-only `responses_template.csv`. No responses were entered or generated.
- `AGENT_BRIEFING.md` added for agents joining the project.
- Full handoff: `handoffs/claude-t02-20261117-004.md`.

### claude-t02-20261117-005

- Agent: claude-t02 (AI assistant). Status: ready_for_review. Responds to the integration review on PR 2 (comment of 17 Nov 2026, head 6c75387).
- Blocking 1: `works.json` now holds one record for each of the 212 distinct works (126 with an arXiv ID, 86 without). The count is the number of distinct work IDs; the build and both audits assert that records − repeats − unverified equals it.
- Blocking 2: P011 is `queued_not_read_access_refused` and P017 is `not_queued_awaiting_full_text`; both counts are derived from those decisions. No count in `build_t02.py` is typed.
- Blocking 3: `repeat_discovery_of` is removed. `work_id` holds work IDs only; `repeat_of_record` and `possible_duplicate_of` hold record IDs only; `check_corpus.py` validates every target.
- Blocking 4: `.github/workflows/checks.yml` added (corpus audit, structural manuscript audit, questionnaire regeneration and consistency).
- Follow-ups: Table VIII restored to 12 rows, three per category (Q007 closed); published-record DOIs added to 10 references with the venue policy stated in Section II.C (Q008 decided); audit wording changed to "numeric strings found in locally saved text".
- T13 remains OPEN: OpenAI's technical report is on a host outside the network allowlist; the request to add it was not answered.
- Draft v0.5 in `paper/`. Audit output: `evidence/audit_paper_output_20261117.txt`.

### claude-t02-20261117-006

- Agent: claude-t02 (AI assistant). Status: ready_for_review.
- T13: OpenAI's technical report (38 pages) retrieved after `cdn.openai.com` was added to the allowlist. Read in part: contents, introduction, and targeted comparison with the operator's post. Ledger entries I30–I35 added (35 entries in total).
- No disagreement found between the post and the report on the statements the paper uses. The report agrees with Hugging Face that agents inferred the platform might hold solutions, and records agent requests to Hugging Face as early as 26 May 2026.
- The paper text is unchanged: the report is not cited (references are at 40) and nothing it says contradicts Section V.D. Black Hat talk still not accessed.

### COORD-20261117-002

- Agent: ChatGPT coordinator; task: second integration review of PR 2 at commit `224f3a7`; status: accepted after state synchronization.
- Independently reconciled 234 discovery records, 18 repeat records, 4 unverified records and 212 unique work IDs. All 212 verified canonical records map one-to-one to `works.json`.
- Confirmed the explicit unread decisions: P011 is queued but unread because access was refused; P017 was not queued and awaits full text.
- Confirmed 35 included works (A 10, B 9, C 8, D 8), 35 incident-ledger claims, 40 references, Table VIII with 12 rows (three per category), and a header-only questionnaire response template.
- Confirmed GitHub Actions run 44029147888 passed the corpus, structural manuscript and questionnaire checks on commit `224f3a7`.
- Accepted venue policy: claims remain tied to the pinned arXiv version read; verified published-record metadata may be added without claiming the published text was examined.
- Remaining human gates: reading included papers, semantic/second-reader checking of quoted numbers, questionnaire approval before distribution, identity/course/declaration fields and supervisor review.

### COORD-20261117-003

- Agent: ChatGPT coordinator; task: T09 independent second-reader batch 1; status: in progress on branch `chatgpt/t09-second-reader-batch1`.
- Checked W045, W021, W103 and W012 against their pinned primary-source versions and re-evaluated the three-work adaptive-attacker count behind F3.
- Confirmed four checks and found one semantic error: the manuscript pairs 96% and 17% from different W021 protocols. The correct resample-then-defer comparison is 89% to 17%; the separate defer-on-critical configuration is 96% against its default attack and 100% against the strengthened attacks tested.
- Evidence and locators: `evidence/second_reader/t09_batch1_20261117.md`.
- Next action: patch all source representations, rebuild DOCX/PDF, rerun audits, then continue with F6 utility reporting.
