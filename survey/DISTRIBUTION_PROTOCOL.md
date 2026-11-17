# Questionnaire approval and distribution protocol

Status: preparation only. **Do not recruit participants or publish a form until the supervisor has approved the instrument and confirmed whether university ethics review or an exemption is required.**

This protocol applies to questionnaire v0.2 in this repository. It does not authorize data collection.

## 1. Approval packet for the supervisor

Send these files together:

1. `survey/QUESTIONNAIRE.md` — participant-facing wording.
2. `survey/README.md` — purpose, sampling limits and analysis plan.
3. `survey/questionnaire.csv` and `survey/codebook.csv` — form specification and response coding.
4. This distribution protocol.
5. A one-page request stating:
   - the project is a B.Tech literature survey with a small practitioner side instrument;
   - respondents will be adults (18+);
   - participation is voluntary;
   - no names, e-mail addresses, employers, account identifiers or credentials will be requested;
   - the planned sample is a non-probability convenience sample;
   - no questionnaire result will be reported as representative of all developers or AI users.

Ask the supervisor in writing:

- May the 5–8 person comprehension pilot begin?
- Is Research Advisory/Ethics Committee review required, or may the project proceed under a written class-project exemption?
- Which form platform and university account should store the responses?
- What retention period and deletion date should be used?
- May student groups and external developer communities be approached?

Keep the approval message in the project records.

## 2. Consent wording issue to resolve before approval

The current information screen says, “we do not record your IP address.” A third-party form platform may process technical logs even when the researcher cannot see them. Do not promise platform behaviour that has not been verified.

Preferred wording:

> We do not ask for your name, e-mail address, employer or account details. The response file available to the student research team will not contain these identifiers. The form provider may process technical data under its own privacy policy.

The supervisor should approve the final privacy wording.

## 3. Build the form

Use a university-approved Google Forms, Microsoft Forms or equivalent account.

### Required settings

- Do not collect e-mail addresses.
- Do not require sign-in unless the approved protocol explicitly permits it.
- Do not limit to one response if that requires identity collection.
- Do not collect file uploads.
- Do not request names, URNs, phone numbers, employers, credentials or free-form contact details.
- Consent/age confirmation is required to continue.
- Every substantive research question is optional.
- Disable public response summaries.
- Do not publish respondent-level spreadsheets.
- Give the supervisor access to the form and storage location.

### Sections and branching

1. Information and consent.
2. Section A: all eligible participants.
3. Section B: show only if A2 is not “Never”.
4. Show B5 only if B4 is “Yes”.
5. Sections C and D.
6. Show D4 only when its stated condition is met.
7. Completion page with the student and supervisor contact details.

Build the form from `survey/questionnaire.csv`; use `show_if` for branching and `codebook.csv` for response coding.

### Randomisation

Randomise C3 statements and most/least options only if the platform can preserve a consistent option order across each paired “most” and “least” item. Otherwise use one fixed, pre-randomised order and document it.

## 4. Pilot before recruitment

After approval, invite 5–8 adults for a comprehension pilot.

Ask each pilot participant:

- What did you think each question was asking?
- Which words were unclear?
- Did any answer option feel missing or overlapping?
- Did the branching behave correctly?
- How long did completion take?

Pilot responses are usability evidence, not research results. Do not combine them with the final dataset. Revise the wording, increment the questionnaire version, obtain supervisor confirmation and freeze the final instrument.

## 5. Recruitment

Recommended final target: at least 60 valid responses, while describing the sample as a convenience sample.

Possible channels, only after approval:

- IILM adult students who have used action-taking AI agents;
- IEEE/ACM or coding-club groups;
- hackathon and developer communities;
- security or AI practitioner groups approved by the supervisor.

Avoid:

- implying participation affects marks, membership or opportunities;
- repeated direct messages to people who do not respond;
- recruiting anyone under 18;
- promising anonymity if the selected platform exposes identifiers;
- paid incentives or prizes unless specifically approved.

## 6. Invitation template

> **Voluntary 5–6 minute student research questionnaire: AI agents**
>
> I am conducting a supervised B.Tech research project at IILM University about how people use AI agents that can take actions, such as running commands, editing files or using browser tools.
>
> If you are 18 or older, you are invited to complete a short voluntary questionnaire. It does not ask for your name, e-mail address, employer, credentials or account details. You may skip any research question or stop at any time.
>
> The responses will be analysed as a convenience sample and reported only in aggregate. Completing the form will not affect grades, club membership or access to any opportunity.
>
> Researcher: [student name and IILM e-mail]  
> Supervisor: [name and IILM e-mail]  
> Form: [approved link]  
> Closing date: [date]

Do not insert or circulate a form link until approval is recorded.

## 7. Data handling

When data collection closes:

1. Export the platform response file once as the immutable raw copy.
2. Store it in the supervisor-approved location with restricted access.
3. Create a separate analysis copy; never edit the raw file.
4. Check that no platform-added identifiers or timestamps violate the approved plan.
5. Assign study IDs if needed; do not create a re-identification key unless approved.
6. Record exclusions and missing-response denominators.
7. Report counts and percentages with the number answering each item.
8. Do not run significance tests on the 5–8 person pilot.
9. Apply the approved retention and deletion schedule.

## 8. Reporting boundary

Until real, approved responses exist:

- `survey/responses_template.csv` remains header-only;
- the literature findings must not be described as questionnaire findings;
- no simulated, estimated or AI-generated response may enter the dataset;
- the paper may say only that the questionnaire was drafted and not administered.

## Institutional references

- IILM University Gurugram, Code of Ethics for Research: https://iilm.edu/gurugram/code-of-ethics-for-research/
- IILM University Research Policy: https://iilm.edu/wp-content/uploads/2026/03/IILM-University-Research-Policy.pdf
