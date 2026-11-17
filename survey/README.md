# Practitioner questionnaire: purpose, safeguards and plan

Status: **draft v0.1, not administered. No responses exist and none are reported anywhere in the review.**

## Why it exists

The review found that evidence linking laboratory results to what happens in use is thin (gap G5). This questionnaire is a small first step towards that link: it asks people who use or build AI agents what permissions they grant, how they check an agent's work, which failures they expect, and which safeguards they use. It is a side piece. The review's findings rest on the papers it read; the questionnaire neither supports nor tests them yet.

This reverses decision D001 on the message board ("no participant survey"), on the student's instruction of 17 November 2026. It does not reverse D002: the review is still a literature survey.

## Design choices

- **Almost no typing.** 16 of 17 items are closed: single choice, multiple choice, a six-statement agreement scale, and four "most / least" items. One optional one-line answer at the end.
- **Most/least items instead of long rating grids.** Picking the most and least likely of four or five options is quick, forces a choice, and avoids everyone rating everything "important".
- **Plain language.** The four failure types are the review's categories A–D rewritten without jargon. No item uses "rogue", "scheming" or other loaded words.
- **Statements that can be disagreed with.** In C3 the reviewed work gives reasons to doubt statements s1–s5, so agreement is the informative answer. They are worded neutrally and should be shown in random order.
- **About five minutes.** Section B is skipped for people who have never used an agent.

## Before anyone is asked to answer it

1. **Supervisor approval.** Show the questionnaire and this page to the supervisor and follow whatever the institute requires for collecting responses from people. Do not distribute it before that.
2. **Fill the contact placeholders** on the information screen.
3. **Form settings:** do not collect e-mail addresses or sign-ins; allow every question to be skipped; randomise the order of options in the most/least items and of the statements in C3; show B5 and D4 only when their conditions are met.
4. **Pilot with 5–8 people** who then say aloud what each question meant to them. Fix wording, then freeze the version number.

## What will and will not be claimed

- Respondents will be whoever can be reached (classmates, developer groups). That is a convenience sample: results describe those respondents only, not "developers" or "users" in general.
- Report counts and percentages with the number who answered each item. For most/least items report, per option, (times chosen most − times chosen least) ÷ respondents.
- No significance tests at pilot size. Comparisons between groups (for example students vs practitioners) are exploratory and need at least 30 per group before they are even described.
- Self-reports of unauthorized actions (B4, B5) are recollections, not measurements of how often such actions occur.
- Never enter, estimate or simulate responses. An empty results table is the truthful state until people have answered.

## Planned use in the review

- **Now (v0.4 of the paper):** one sentence under Future Directions says the instrument exists and has not been administered.
- **After a pilot:** still no results in the paper; only wording changes here.
- **After a real round (target 60+ responses):** a short subsection or appendix comparing stated practice with findings F1–F6, clearly separated from the literature evidence, with the limits above.
- **Later:** repeat after major incidents or tool changes to see whether practice moves; add items generated from E1; translate if the audience requires it.

## Files

| File | Purpose |
|---|---|
| `QUESTIONNAIRE.md` | The questionnaire as participants would see it, plus the item map |
| `questionnaire.json` | The same items in machine-readable form, for coding responses |
| `build_questionnaire.py` | Single source for both files |
| `responses/` | Does not exist yet. Create only when real, anonymised responses are exported |
