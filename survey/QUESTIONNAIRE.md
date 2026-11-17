# Practitioner questionnaire on unauthorized actions by AI agents

Version 0.1 | 17 November 2026 | **DRAFT - not administered; no responses exist**

A side instrument to the literature review, not part of its evidence. It asks people who use or build AI agents what they do and expect, so that later versions of the review can compare practice with what the reviewed papers found. See `survey/README.md` for purpose, ethics, analysis plan and growth plan.

17 items, 16 of them closed (single choice, multiple choice, agreement scale, or most/least); about 5-6 minutes; no typing required.

## Information for participants (first screen)

> This short questionnaire is part of a student project at IILM University on how people use AI agents that can take actions, and what can go wrong. It takes about five minutes and almost every question is a single click.
>
> Taking part is voluntary. You may stop at any time by closing the page, and you may skip any question. We do not ask for your name, e-mail address, employer or any account details, and we do not record your IP address. Answers are stored without identifiers and reported only as totals.
>
> You must be 18 or older to take part. Contact for questions: **[ name and institute e-mail of the responsible student ]**; supervisor: **[ name ]**.
>
> ☐ I am 18 or older and I agree to take part. *(required to continue)*

## A. About you

**A1.** Which best describes you?

- ○ Student
- ○ Software developer or engineer
- ○ Security professional
- ○ Researcher or academic
- ○ Manager or other professional
- ○ Prefer not to say

**A2.** How often do you use an AI agent that can take actions for you (run commands, edit files, browse, send messages), as opposed to a chat assistant that only answers?

- ○ Never
- ○ I have tried one a few times
- ○ A few times a month
- ○ A few times a week
- ○ Daily
- ○ I build or deploy such agents

**A3.** Which kinds of agent have you used? Select all that apply.

- ☐ Coding agent with terminal or file access
- ☐ Browser or computer-use agent
- ☐ E-mail, calendar or office assistant that can act
- ☐ Several agents working together
- ☐ None of these

## B. How you use agents

**B1.** What is the most powerful thing you have allowed an agent to do without asking you first?

- ○ Nothing: it only suggests, I act
- ○ Read files or web pages
- ○ Edit files in one project folder
- ○ Run commands on my machine
- ○ Use my accounts, credentials or payment details
- ○ Not sure

**B2.** Where does the agent usually run?

- ○ Directly on my own computer
- ○ In a container or virtual machine
- ○ In a cloud sandbox provided by the tool
- ○ Not sure

**B3.** When an agent says a task is finished, what do you usually do?

- ○ Accept its summary
- ○ Skim what it changed
- ○ Run my own tests or checks
- ○ Review the changes line by line
- ○ It depends on the task

**B4.** Has an agent you were using ever done something you had not authorized?

- ○ No
- ○ Yes, something minor
- ○ Yes, something with real consequences
- ○ Not sure

**B5.** If yes: what happened? Select all that apply. *(shown only if B4 is 'Yes')*

- ☐ Changed or deleted files outside the task
- ☐ Altered a test or check so that it passed
- ☐ Followed instructions found in a page, document or message
- ☐ Used the network, an account or a credential unexpectedly
- ☐ Reported success when the task had not been done
- ☐ Something else

## C. What you expect

**C1.** Think about your own use of agents over the next year. Which of these is MOST likely to happen, and which is LEAST likely?

| Most | | Least |
|:---:|---|:---:|
| ○ | The agent makes its result look successful without doing the task as intended (for example, changing a test or check so that it passes). | ○ |
| ○ | The agent follows instructions hidden in something it reads (a web page, e-mail, document or tool output) instead of the user's instructions. | ○ |
| ○ | Several agents pass each other content or permissions so that one does something none was individually allowed to do. | ○ |
| ○ | The agent does something outside its task and the monitoring or review in place does not catch it. | ○ |

*Choose exactly one in each column.*

**C2.** If each of these did happen, which would do the MOST harm, and which the LEAST?

| Most | | Least |
|:---:|---|:---:|
| ○ | The agent makes its result look successful without doing the task as intended (for example, changing a test or check so that it passes). | ○ |
| ○ | The agent follows instructions hidden in something it reads (a web page, e-mail, document or tool output) instead of the user's instructions. | ○ |
| ○ | Several agents pass each other content or permissions so that one does something none was individually allowed to do. | ○ |
| ○ | The agent does something outside its task and the monitoring or review in place does not catch it. | ○ |

*Choose exactly one in each column.*

**C3.** How far do you agree with each statement?

| | Strongly disagree | Disagree | Neither agree nor disagree | Agree | Strongly agree |
|---|:---:|:---:|:---:|:---:|:---:|
| A published attack-success rate for an agent tells me how safe it will be in my own setting. | ○ | ○ | ○ | ○ | ○ |
| If an agent's work passes its tests, the task has been done as intended. | ○ | ○ | ○ | ○ | ○ |
| A safeguard that works for one agent will also work when several agents work together. | ○ | ○ | ○ | ○ | ○ |
| An automated monitor can be relied on to catch an agent that acts outside its task. | ○ | ○ | ○ | ○ | ○ |
| More capable models are less likely to take unauthorized shortcuts. | ○ | ○ | ○ | ○ | ○ |
| I would accept an agent being slower or less capable in exchange for stronger safeguards. | ○ | ○ | ○ | ○ | ○ |

**C4.** An agent is given a task that turns out to be impossible as stated. Which is it MOST likely to do, and which LEAST likely?

| Most | | Least |
|:---:|---|:---:|
| ○ | Stop and report that the task cannot be done | ○ |
| ○ | Keep trying within the rules until it runs out of time | ○ |
| ○ | Change the test or check so that the task appears done | ○ |
| ○ | Look for the answer somewhere it was not meant to access | ○ |

*Choose exactly one in each column.*

## D. Safeguards

**D1.** Which of these safeguards matters MOST, and which LEAST, for using agents safely?

| Most | | Least |
|:---:|---|:---:|
| ○ | Running the agent in an isolated environment with no access to the wider network | ○ |
| ○ | Giving the agent only the narrow permissions and credentials the task needs | ○ |
| ○ | Requiring a person to approve risky actions before they run | ○ |
| ○ | Having a second automated system monitor the agent's actions | ○ |
| ○ | Testing the agent against deliberate attempts to break the safeguards before using it | ○ |

*Choose exactly one in each column.*

**D2.** Which of these have you actually used? Select all that apply.

- ☐ Running the agent in an isolated environment with no access to the wider network
- ☐ Giving the agent only the narrow permissions and credentials the task needs
- ☐ Requiring a person to approve risky actions before they run
- ☐ Having a second automated system monitor the agent's actions
- ☐ Testing the agent against deliberate attempts to break the safeguards before using it
- ☐ None of these

**D3.** Before this questionnaire, had you heard of the July 2026 incident in which AI agents under evaluation intruded into the Hugging Face platform?

- ○ No
- ○ I had heard of it
- ○ I have read one of the published reports

**D4.** If you had heard of it: did it change how you use or configure agents? *(shown only if D3 is not 'No')*

- ○ No
- ○ A little
- ○ Substantially
- ○ I do not use agents

## E. Optional

**E1.** Optional, one line: is there anything about agents acting without authorization that these questions missed?

`____________________________________________` *(optional)*

## Closing screen

> Thank you. Your answers have been recorded without any identifying information.

## Item map (not shown to participants)

| Item | Type | What it measures, and the review question, gap or finding it relates to |
|---|---|---|
| A1 | single | sample description |
| A2 | single | exposure; skip logic: 'Never' skips section B |
| A3 | multi | exposure |
| B1 | single | permissions (RQ1; finding F2) |
| B2 | single | isolation in practice (gap G1; finding F2) |
| B3 | single | outcome verification independent of the agent's narrative (category A) |
| B4 | single | self-reported incidence (RQ3; gap G5) |
| B5 | multi | mechanism (RQ1; categories A, B, D) |
| C1 | bestworst | perceived likelihood by category A-D (RQ1) |
| C2 | bestworst | perceived severity by category A-D |
| C3 | likert | s1: F1/G2; s2: category A; s3: F4/G4; s4: F2/F3; s5: capability and gaming (A); s6: security-utility trade-off (F6). The reviewed work gives reasons to doubt s1-s5; agreement is therefore the informative response. |
| C4 | bestworst | finding F5; motivating incident |
| D1 | bestworst | perceived priority vs findings F2, F3 |
| D2 | multi | adoption vs stated priority (D1) |
| D3 | single | awareness (RQ3) |
| D4 | single | incident-to-practice link (gap G5) |
| E1 | text | item generation for the next version |

Category letters, gap numbers (G1–G5) and finding numbers (F1–F6) refer to Sections III, V.E and VI of the review.
