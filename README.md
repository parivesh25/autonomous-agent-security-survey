# Autonomous-agent security survey

Evidence-traceable literature survey for Foundations of Cybersecurity (CSE25305), IILM University, Gurugram.

## Current paper: v0.7

- [PDF](paper/AgentSecuritySurvey_v0.7.pdf)
- [Overleaf / editable LaTeX ZIP](paper/AgentSecuritySurvey_v0.7_Overleaf.zip)
- [LaTeX source and editing instructions](paper/latex_v0.7/README.md)

The v0.7 source preserves the author's manually edited DOCX and is now the canonical manuscript. Legacy `MANUSCRIPT.md`, `paper/content.py` and `tools/build_paper.py` document/rebuild v0.6; they do not regenerate v0.7. Research tables and numerical claims were checked against the edited draft during conversion. The bibliography contains 40 references; the included corpus contains 35 works with AI-assisted extraction of logged sections.

Reported human reading: Parivesh Singh 7 works, Vaibhav Gaur 3. Work IDs and overlap have not been supplied, so these must not be described as 10 distinct completed human reviews. Human reading, source verification, signatures and supervisor review remain outstanding. Draft integration does not certify academic submission readiness.

The practitioner questionnaire in `survey/` is a side instrument, not administered. Supervisor approval is required before distribution. No responses or results exist.

## Reproduce checks

Run `python tools/check_corpus.py`, `python tools/audit_paper.py --structural`, `python tools/check_questionnaire.py` and `python tools/check_latex_v07.py`. The first two manuscript-source checks cover legacy evidence/claim sources; the v0.7 checker covers canonical LaTeX, and `evidence/audit_v07_conversion.json` records preservation of the edited DOCX's claims and table cells.

Compile with XeLaTeX (`latexmk -xelatex main.tex` inside `paper/latex_v0.7`). The release workflow re-fetches pinned sources and reruns the numeric string-presence check. String matches are not semantic verification or human reading. See `AGENT_BRIEFING.md`, `MESSAGE_BOARD.md` and `handoffs/` for coordination and remaining tasks.
