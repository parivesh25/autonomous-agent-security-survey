# Release handoff: LaTeX v0.7 (PR 4)

```
message_id: claude-release-20261118-001
board_version_read: 0.4 (plus messages up to COORD-20261117-005)
agent_id: Claude (AI assistant working for Paarv; not an author)
task: finish v0.7 verification and release, on Paarv's instruction of 18 Nov 2026
input handoff: handoffs/chatgpt-to-claude-v07-20261118.md (including Paarv's edit fa2e416)
status: released on PR 4
```

## Source changes in this pass

| Commit | Change |
|---|---|
| eceb6da | Merged the handoff branch (`chatgpt/v07-claude-handoff-20261118`, PR 6) into the PR 4 branch, bringing the handoff file and Paarv's supervisor-name edit |
| 046fe0a | Applied that edit to the paper: supervisor **Dr. Abhishek Pandey** on the cover and in the acknowledgment. Confirmed e-mail `abhishek.pandey@iilm.edu` and the blank assessment marks are unchanged. `tools/check_latex_v07.py` now asserts the name, the e-mail and blank marks |
| 3957879, 046fe0a, 9c3b138 | Release workflow: longer install limits; `tex-gyre` and `fonts-texgyre` added (see CI below) |

No research text, number, table cell or reference was changed. The historical board messages and the v0.6 snapshot (`tools/build_paper.py`, which still names the earlier supervisor spelling) were left as they are; v0.6 is not the canonical source.

## How the release artifacts were built

The CI release job never completed on this branch after the continued-header change (cd0d29b):

| Run | Head | Failure |
|---|---|---|
| 44218655741 | df8ba98 | TeX install timed out after 6 minutes (slow runner mirror) |
| 44223481403 | 3957879 | XeTeX could not find TeX Gyre Termes (`--no-install-recommends` drops the fonts) |
| 44224339405 (PR 6) | fa2e416 | same font error |
| 44224827004 | 046fe0a | same font error: `tex-gyre` alone does not register fonts with fontconfig |
| 44228415505 | 9c3b138 | font packages now included, but the 146 MB download exceeded the 20-minute limit (mirror served ~100 kB/s) |

The artifacts were therefore built locally with the same toolchain the workflow uses (Debian TeX Live 2025, XeLaTeX via latexmk, TeX Gyre Termes because Times New Roman is not installed), following the workflow's steps one by one, and committed with `[skip release]` so the workflow does not try to rebuild them.

Cross-check against the last CI-built release (2b20a6e): the 15 page renders were regenerated at the workflow's settings; **11 are byte-identical to the CI renders**, and the 4 that differ are exactly the pages whose source changed: 1 (supervisor name), 7 and 8 (continued table headers, cd0d29b) and 11 (acknowledgment).

## Results

| Check | Result |
|---|---|
| `tools/check_latex_v07.py` | PASS: 40 resolved references, 11 tables, 3 figures, 8 sections; abstract 239 words; F6 15/35 and W021 89% to 17% retained; supervisor name, e-mail and blank marks asserted |
| Pages | 15 PDF pages: cover 1, paper 2–13 = **12 pages**, annexure 14–15 |
| LaTeX log | no undefined references or citations, no missing glyphs, 0 overfull boxes |
| `tools/audit_paper.py --structural` | PASS |
| `tools/check_corpus.py` | PASS (234 records, 18 repeats, 4 unverified, 212 works) |
| `tools/check_questionnaire.py` | PASS: 17 items, 79 option rows, 42 columns, 0 answer rows |
| Numeric-string audit | 106 of 106 strings found. 103 in text re-fetched by `tools/fetch_v07_audit_sources.py` (all 35 arXiv PDFs and 4 incident pages); 3 (198, 898, 93) in the saved copy of OpenAI's post that Paarv supplied on 16 Nov, because openai.com still returns 403. CI previously reported these three as not found; the targeted semantic check is `evidence/second_reader/t09_openai_numbers_20261117.md`. A string match is not semantic verification or human reading |
| LaTeX to v0.6 number parity | Every number in `manuscript.tex` also appears in the audited v0.6 text; the only differences are layout parameters and front-matter metadata |
| W021 correction | Re-confirmed in the source text: Table 1 gives resample-then-defer 0.89 (default) and 0.17 (monitor simulation); Table 2 gives defer-on-critical 0.96 and 1.0 |
| Overleaf ZIP | 12 files (all .tex/.png/.md/.json in `paper/latex_v0.7/`); every entry byte-identical to the source; no build auxiliaries |
| Visual QA | All 15 pages rendered and inspected; continued table headers on pages 7–8 now print as bold text; no clipping or overlap found |

PDF SHA-256: `fd87a286ea2ae1c522f803fb8287628aca3cbc2e3dab72ee384b56c5f39350dc`
ZIP SHA-256: `9860b231e595f9dc91525f999c0fba27cf21d96acfdfe245b0a997fb3c98e3eb`

## What remains, unchanged by this release

- Human reading: reported 7 (Parivesh Singh) and 3 (Vaibhav Gaur); work IDs and overlap unknown, so not 10 distinct works. No per-work human flag was changed.
- Human second-reader confirmation of quoted numbers; human originality and spell review.
- Declaration and signatures; assessment marks intentionally blank; submission date kept at 17 November 2026 as the author edited it.
- Supervisor approval of the questionnaire before distribution; no responses exist.
- Black Hat talk not accessed; OpenAI technical report read only in part.
- The CI release job still needs a reliable TeX install (the runner's Ubuntu mirror is the bottleneck). Until then, build locally or in Overleaf (XeLaTeX, `main.tex`) and commit with `[skip release]`.
