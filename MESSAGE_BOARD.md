# Research coordination message board

Project AGENT-SEC-SURVEY | Version 0.1 | Updated 16 November 2026

**State:** pilot discovery complete; full-text screening and synthesis pending. This is a portable board snapshot. No external agents are connected automatically. Paarv or a designated coordinator is the single merge authority until a shared repository is configured.

## Decisions

| ID | Decision | Basis |
|---|---|---|
| D001 | Literature survey; no participant survey | Professor's template |
| D002 | Incident is a motivating example, not the entire corpus | Need comparison across at least 25 works |
| D003 | Pilot period 2023–16 Nov 2026; older exceptions documented | Keeps scope manageable; date verification required |
| D004 | Do not pool incomparable attack-success rates | Different tasks, threat models and denominators |
| D005 | Separate agent-assisted reading from student reading | Template's declaration and viva requirements |
| D006 | Keep stable paper IDs until final reference numbering | Prevent citation collisions across agents |

## Task queue

All roles below are **unassigned**, not launched agents. Claim by posting a unique message ID. The coordinator acknowledges ownership before concurrent work on the same records.

| Task | Suggested role | Scope | Deliverable | Status |
|---|---|---|---|---|
| T01 | Search and screening lead | Extend pilot, verify dates/versions and duplicates | Updated search log, decisions and eligible corpus | OPEN |
| T02 | Objective-integrity reviewer | P001–P010, plus targeted foundational studies | Methods/results/limitations extraction and category comparison | OPEN |
| T03 | Authorization reviewer | P011–P020; AgentDojo, ASB and isolation defenses | Extraction with attacker model and utility costs | OPEN |
| T04 | Multi-agent/control reviewer | P021–P030; monitoring and coordination literature | Extraction distinguishing single-run and collective outcomes | OPEN |
| T05 | Incident evidence reviewer | Operator, affected-platform and independent reports | Dated claim ledger; disagreements and visibility limits | OPEN |
| T06 | Data and synthesis reviewer | Merged included corpus after T01–T04 | Valid comparison tables and three figure datasets | WAITING |
| T07 | Manuscript editor | Evidence accepted by reviewer | Template-compliant draft, DOCX/PDF and reference cross-check | WAITING |

For a four-person student team, combine T01/T06/T07 as coordination duties and distribute literature categories among all members. Every student must read papers, not merely format a section.

## Known issues

| Issue | Required action | Owner |
|---|---|---|
| Q001 P004/P006 have matching normalized titles | Confirm work/version identity; retain both discovery records | T01 |
| Q002 Discovery strongly favors 2026 results | Add earlier-year and exact-title searches; do not infer a publication trend from this sample | T01 |
| Q003 ASB descriptions vary between versions | Pin a primary version before extracting benchmark counts | T03 |
| Q004 Taxonomy overlap | Assign by principal evaluated boundary; secondary tags allowed | Coordinator |
| Q005 No shared repository destination yet | Use handoff-only mode; do not assume cross-chat synchronization | Paarv |
| Q006 No final inclusion count or reading-compliance count | Complete reading gates before filling abstract/selection diagram | T01 |

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
- Q004: adjudication requested for W017, W115, W110, W111.
- Q005: a shared repository now exists; coordinator to update.
- Q006: unchanged. Abstract screening gives a 43-work reading queue (A 11, B 13, C 9, D 10). Works read in full: 0. Works included: 0.
- Full handoff: `handoffs/claude-t01-20261116-001.md`.
- Next action: coordinator review; T02-T04 full-text reading at pinned versions; T05 incident ledger.
