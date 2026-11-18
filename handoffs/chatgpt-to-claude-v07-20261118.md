# Claude takeover — LaTeX v0.7 release
Date: 18 November 2026. ChatGPT paused at the user's explicit request. No PR was merged during this work.

## Start here
- Repository: https://github.com/parivesh25/autonomous-agent-security-survey
- Active paper branch: `chatgpt/t09-second-reader-batch1`
- Open draft PR: https://github.com/parivesh25/autonomous-agent-security-survey/pull/4
- Last observed active-branch head: `df8ba980f4cf772f1659a48fd2a5112239461fe3`.
- PRs 1, 2, 3 and 5 are already merged. PR 4 is the only open PR.
- This handoff is on a separate documentation branch, `chatgpt/v07-claude-handoff-20261118`, to avoid moving the branch under running build jobs. Continue the paper on the ACTIVE PAPER BRANCH above, not this snapshot branch. Fetch fresh state first; Actions may append artifact commits.
- Read `AGENT_BRIEFING.md`, `MESSAGE_BOARD.md`, and `paper/latex_v0.7/README.md`. The briefing contains an explicitly historical v0.6 section; its old zero-human-reading status is superseded by the current reported aggregate counts below.

## User's requested outcome and authority
Produce corrected v0.7 in LaTeX from the user's manually edited v0.6 DOCX, follow the professor's format, inspect the changed pages, keep the paper within 12 pages, rerun structural/numeric audits, check the checklist, and finish the outstanding PR merges. The user explicitly authorized merging; do so only after the final sources/artifacts and checks reconcile. This pause delegates completion to Claude; it is not permission to certify uncompleted human academic work.

## Work completed
1. Downloaded and converted the actual author-edited `AgentSecuritySurvey_draft_v0.6-edited(1).docx`, not the old generated DOCX. Source SHA256: `e2a9d47ef8b750d6df9ee16ba69795077e996bf81255778eda21c5fc71d784b7`. Original ChatGPT Library ID: `libfile_f6be3984903c81918b0a40ebb5825595`. The original need not be downloaded again to continue; converted source is committed.
2. Created canonical, independently editable LaTeX project `paper/latex_v0.7/`:
   - `main.tex`, `format.tex`, `cover.tex`, `manuscript.tex`, `references.tex`, `annexure.tex`
   - `selection-flow.tex` (native TikZ), `figures/`, `README.md`, `provenance.json`.
3. Preserved research claims and table values. `evidence/audit_v07_conversion.json` records 46 narrative paragraphs preserved, all 11 tables checked cell by cell, and 40 reference entries retained. Abstract spelling changed only from “Defenses” to “Defences”. Later layout edits shortened the Table VIII header “Category” to “Cat.” and clarified Figure 1 labels without changing counts.
4. Corrected paper authors to Parivesh Singh and Vaibhav Gaur. Supervisor appears on the cover, not as an unrequested third author. Corrected affiliation punctuation. Replaced acknowledgment placeholder with a short acknowledgment. Retained the author's contribution assignments.
5. Preserved the user-confirmed supervisor details and intentionally blank assessment marks. Updated declaration/checklist so they do not falsely certify completed human reading.
6. Improved Figure 1 labels: titles plus available abstracts were screened; included works received AI-assisted review of logged sections, not a blanket cover-to-cover reading claim. Enlarged taxonomy/trend figures for readability.
7. Added `.github/workflows/build-paper-v07.yml`, `tools/check_latex_v07.py`, and `tools/fetch_v07_audit_sources.py`. The workflow compiles, audits, renders every page, packages an Overleaf ZIP, and commits generated outputs.
8. Updated README, AGENT_BRIEFING and appended board message COORD-20261117-005. Legacy `tools/build_paper.py`, `paper/content.py`, and `MANUSCRIPT.md` remain v0.6 snapshots. DO NOT run them to overwrite v0.7. The old v0.6 workflow skips when the v0.7 source exists.

## Metadata that must not be “corrected” away
- Parivesh Singh, URN 2581138, parivesh.singh.ug25@iilm.edu
- Vaibhav Gaur, URN 2581149, vaibhav.gaur.ug25@iilm.edu
- Course: Foundations of Cybersecurity; CSE25305
- Supervisor: Dr. Abhishek Pandey
- Supervisor email: abhishek.pandey@iilm.edu — explicitly confirmed by the user despite the surname mismatch
- Designation: Assistant Professor, School of Computer Science and Engineering
- Course coordinator: Dr. Preetisha
- B.Tech (CSE), Semester III; Batch 2025–29; Session 2026–27; Team G-08
- Assessment: Project (End Semester Evaluation, ___ Marks). Marks intentionally unknown; leave blank.
- Author-edited submission date: 17 November 2026. Do not silently replace with today's date.

## Research integrity / counts
- 234 discovery records − 18 repeats − 4 unverified = 212 distinct works.
- Reading queue 43 = 35 included + 7 read but not included + 1 unread.
- Included categories A 10, B 9, C 8, D 8. Bibliography 40 references.
- Table VIII: 12 works, three per category; paper has 11 tables and 3 figures.
- T09 F6 semantics were already checked: legitimate-task utility is 15/35, split A 2/10, B 5/9, C 2/8, D 6/8. W003 runtime overhead alone is NOT utility.
- W021 correction retained: resample-then-defer safety 89% against default attack versus 17% with monitor simulation; 96% belongs to a DIFFERENT defer-on-critical configuration.
- The author's edited contribution table reports human reading counts of 7 for Parivesh and 3 for Vaibhav. Work IDs and overlap are unknown; do not infer 10 distinct works or modify per-work human flags. The user asked to match these to AI reading and said they would catch up later. ChatGPT explicitly kept completed human reading separate from planned reading: 35 included AI-assisted extraction reviews, versus reported human counts 7 and 3.
- Human second-reader/source verification is still unconfirmed. Do not sign declarations or fill questionnaire responses.
- Questionnaire remains unadministered, requires supervisor approval before distribution, and has no results.
- Black Hat talk remains unaccessed; OpenAI technical report was read only in part. See prior ledgers/handoffs. Do not close these as completed.

## Last successful PDF and audits — IMPORTANT VERSION DISTINCTION
The last successfully compiled artifacts were committed at `2b20a6e084cee9bc868c110a5d58ca69097605ee`, built from substantive source `ade75636dc0059a02b937c2a171fce17d355a933`.
- `paper/AgentSecuritySurvey_v0.7.pdf`
- `paper/AgentSecuritySurvey_v0.7_Overleaf.zip`
- `evidence/render_v07/page-01.jpg` through `page-15.jpg`
- `evidence/audit_v07_*.txt`, `evidence/v07_latex.log`
- PDF SHA256: `449b78b0137787b377801ab755d803d954526591d962713c1a0190a2006796a1`
- 15 total PDF pages: cover 1; paper 2–13 = EXACTLY 12 pages; annexure 14–15.
- Abstract 239 words; 40 resolved citations; 11 tables; 3 figures; 8 numbered sections; no undefined references, missing glyphs or overfull boxes.
- Structural, corpus and questionnaire checks passed.
- Numeric string-presence audit: 103/106 automatically matched; unmatched 198, 898 and 93 are OpenAI figures covered by the prior targeted semantic-check record `evidence/second_reader/t09_openai_numbers_20261117.md`. Automated fetch could not retrieve that OpenAI page. Do not label this 106/106 automatic or a human second-reader check.

ChatGPT visually inspected ALL 15 pages of that PDF on 18 November. One issue was identified: the continued Table VI header on PDF page 8 appeared as an empty blue strip. Other pages, figures, references, cover and annexure were inspected; no other clipping/overlap was observed.

## The last fix is pushed, but NOT YET built/visually verified
Commit `cd0d29b0b8a54917492de339d79b61c4fd882858`:
- Replaced repeated headers in the four category comparison tables with explicit black bold text on a plain background. First-page headers remain blue/white. This targets the missing continued header.
- Added a build-gate job so commits whose latest message contains `[skip release]` do not trigger another artifact rebuild. Ordinary audit checks still run.
- Do not claim the header fix was visually verified yet.

The first rebuild remained in dependency installation for over 12 minutes:
- Run https://github.com/parivesh25/autonomous-agent-security-survey/actions/runs/44217030953
- Job 134509384940
- Last observed: in_progress, “Install XeLaTeX and audit dependencies”.

Commit `df8ba980f4cf772f1659a48fd2a5112239461fe3` retries installation with:
- DEBIAN_FRONTEND=noninteractive
- --no-install-recommends
- apt network timeouts and one retry
- 180-second apt-update and 360-second install bounds; 10-minute step timeout.
It makes NO paper-content change.
- Retry run https://github.com/parivesh25/autonomous-agent-security-survey/actions/runs/44218655741
- Last observed at handoff: also in_progress at dependency installation.
- Corpus/structural/questionnaire workflow (“checks”) on this head is green; the legacy v0.6 workflow is green/skipped internally.
- Old and retry runs may still be active. Local monitoring has been stopped. Neither run was cancelled. Inspect fresh state before starting further jobs.

Artifact caution: until a successful new build commits outputs, the checked-in PDF/ZIP/audits correspond to the older source above and do NOT contain the latest continued-header change. A successful old runner may fail to push because the branch advanced; do not force-push its stale checkout.

## How to finish
1. Fetch the active branch and inspect both running jobs. Prefer a local XeLaTeX build if available; avoid blindly starting repeated slow CI installs. Browser live logs required sign-in; connector job logs returned 404 while runs were still active. The local execution environment disconnected during the last session, so no alternate local build was completed.
2. Build current source with XeLaTeX:
   `cd paper/latex_v0.7 && latexmk -xelatex -interaction=nonstopmode -halt-on-error main.tex`
   Copy `main.pdf` to `paper/AgentSecuritySurvey_v0.7.pdf`.
3. Rerun `python tools/check_latex_v07.py`, `python tools/check_corpus.py`, `python tools/audit_paper.py --structural`, and `python tools/check_questionnaire.py`. Use the workflow's pinned-source fetch + numeric audit; retain honest coverage/missing-source wording.
4. Render the final PDF and visually verify continued table headers (especially pages 7–8), page breaks, all figures, references, cover and checklist. Confirm paper <=12 pages, excluding cover/annexure. Compare final PDF SHA with the recorded audit and ensure ZIP sources match the built source.
5. Regenerate the Overleaf ZIP from the canonical folder, including all .tex/.png/.md/.json files. Keep build auxiliaries out. The existing workflow performs packaging and rendering.
6. Update the release handoff and append to MESSAGE_BOARD with actual final results. Update PR 4 title/body: it still describes v0.6 and must describe v0.7. Do not rewrite historical board messages.
7. Once source/artifact/checks reconcile, mark PR 4 ready and merge using the expected head SHA. User has already authorized this. Confirm no open PRs remain. Do not merge a stale build or pretend human academic tasks are complete.
8. Give the user final PDF and editable LaTeX/Overleaf ZIP links. Explain that Overleaf must use XeLaTeX and `main.tex`.

## Formatting / editing notes
A4, 2 cm margins, single column, 10.5 pt body, 18 pt paper title, Roman section/table numbers, 9 pt tables/references, numbered citations. Times New Roman is used if installed; TeX Gyre Termes is the portable fallback. No proprietary fonts are redistributed. Check pagination again if changing fonts. References are maintained in `references.tex` with stable `\\cite{rN}` keys, not an external BibTeX dependency.

All substantive work needed to continue is pushed to GitHub. A local-only optional `evidence/human_reading_status.json` was drafted but not pushed; its entire meaning is the 7/3 reported counts and unknown work IDs/overlap described above. It is not needed to build.
