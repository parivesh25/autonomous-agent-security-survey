#!/usr/bin/env python3
"""Single source for the practitioner questionnaire (v0.1, not yet administered).
Writes survey/QUESTIONNAIRE.md (for reading and for pasting into a form tool) and
survey/questionnaire.json (machine-readable, used later to code responses).
Run from the repo root: python3 survey/build_questionnaire.py"""
import json
LIKERT = ["Strongly disagree", "Disagree", "Neither agree nor disagree", "Agree", "Strongly agree"]
FAIL = {  # plain-language forms of the paper's four categories
 "a": "The agent makes its result look successful without doing the task as intended (for example, changing a test or check so that it passes).",
 "b": "The agent follows instructions hidden in something it reads (a web page, e-mail, document or tool output) instead of the user's instructions.",
 "c": "Several agents pass each other content or permissions so that one does something none was individually allowed to do.",
 "d": "The agent does something outside its task and the monitoring or review in place does not catch it.",
}
SAFE = {
 "iso": "Running the agent in an isolated environment with no access to the wider network",
 "priv": "Giving the agent only the narrow permissions and credentials the task needs",
 "appr": "Requiring a person to approve risky actions before they run",
 "mon": "Having a second automated system monitor the agent's actions",
 "adv": "Testing the agent against deliberate attempts to break the safeguards before using it",
}
Q = [
 # ---- A. Background
 dict(id="A1", sec="A. About you", type="single", text="Which best describes you?", options=["Student", "Software developer or engineer", "Security professional", "Researcher or academic", "Manager or other professional", "Prefer not to say"], maps="sample description"),
 dict(id="A2", sec="A. About you", type="single", text="How often do you use an AI agent that can take actions for you (run commands, edit files, browse, send messages), as opposed to a chat assistant that only answers?", options=["Never", "I have tried one a few times", "A few times a month", "A few times a week", "Daily", "I build or deploy such agents"], maps="exposure; skip logic: 'Never' skips section B"),
 dict(id="A3", sec="A. About you", type="multi", text="Which kinds of agent have you used? Select all that apply.", options=["Coding agent with terminal or file access", "Browser or computer-use agent", "E-mail, calendar or office assistant that can act", "Several agents working together", "None of these"], maps="exposure"),
 # ---- B. Practice
 dict(id="B1", sec="B. How you use agents", type="single", text="What is the most powerful thing you have allowed an agent to do without asking you first?", options=["Nothing: it only suggests, I act", "Read files or web pages", "Edit files in one project folder", "Run commands on my machine", "Use my accounts, credentials or payment details", "Not sure"], maps="permissions (RQ1; finding F2)"),
 dict(id="B2", sec="B. How you use agents", type="single", text="Where does the agent usually run?", options=["Directly on my own computer", "In a container or virtual machine", "In a cloud sandbox provided by the tool", "Not sure"], maps="isolation in practice (gap G1; finding F2)"),
 dict(id="B3", sec="B. How you use agents", type="single", text="When an agent says a task is finished, what do you usually do?", options=["Accept its summary", "Skim what it changed", "Run my own tests or checks", "Review the changes line by line", "It depends on the task"], maps="outcome verification independent of the agent's narrative (category A)"),
 dict(id="B4", sec="B. How you use agents", type="single", text="Has an agent you were using ever done something you had not authorized?", options=["No", "Yes, something minor", "Yes, something with real consequences", "Not sure"], maps="self-reported incidence (RQ3; gap G5)"),
 dict(id="B5", sec="B. How you use agents", type="multi", text="If yes: what happened? Select all that apply.", options=["Changed or deleted files outside the task", "Altered a test or check so that it passed", "Followed instructions found in a page, document or message", "Used the network, an account or a credential unexpectedly", "Reported success when the task had not been done", "Something else"], maps="mechanism (RQ1; categories A, B, D)", show_if="B4 is 'Yes'"),
 # ---- C. Expectations
 dict(id="C1", sec="C. What you expect", type="bestworst", text="Think about your own use of agents over the next year. Which of these is MOST likely to happen, and which is LEAST likely?", items=FAIL, maps="perceived likelihood by category A-D (RQ1)"),
 dict(id="C2", sec="C. What you expect", type="bestworst", text="If each of these did happen, which would do the MOST harm, and which the LEAST?", items=FAIL, maps="perceived severity by category A-D"),
 dict(id="C3", sec="C. What you expect", type="likert", text="How far do you agree with each statement?", scale=LIKERT, items={
   "s1": "A published attack-success rate for an agent tells me how safe it will be in my own setting.",
   "s2": "If an agent's work passes its tests, the task has been done as intended.",
   "s3": "A safeguard that works for one agent will also work when several agents work together.",
   "s4": "An automated monitor can be relied on to catch an agent that acts outside its task.",
   "s5": "More capable models are less likely to take unauthorized shortcuts.",
   "s6": "I would accept an agent being slower or less capable in exchange for stronger safeguards."},
   maps="s1: F1/G2; s2: category A; s3: F4/G4; s4: F2/F3; s5: capability and gaming (A); s6: security-utility trade-off (F6). The reviewed work gives reasons to doubt s1-s5; agreement is therefore the informative response."),
 dict(id="C4", sec="C. What you expect", type="bestworst", text="An agent is given a task that turns out to be impossible as stated. Which is it MOST likely to do, and which LEAST likely?", items={
   "stop": "Stop and report that the task cannot be done",
   "try": "Keep trying within the rules until it runs out of time",
   "alter": "Change the test or check so that the task appears done",
   "seek": "Look for the answer somewhere it was not meant to access"}, maps="finding F5; motivating incident"),
 # ---- D. Safeguards
 dict(id="D1", sec="D. Safeguards", type="bestworst", text="Which of these safeguards matters MOST, and which LEAST, for using agents safely?", items=SAFE, maps="perceived priority vs findings F2, F3"),
 dict(id="D2", sec="D. Safeguards", type="multi", text="Which of these have you actually used? Select all that apply.", options=list(SAFE.values()) + ["None of these"], maps="adoption vs stated priority (D1)"),
 dict(id="D3", sec="D. Safeguards", type="single", text="Before this questionnaire, had you heard of the July 2026 incident in which AI agents under evaluation intruded into the Hugging Face platform?", options=["No", "I had heard of it", "I have read one of the published reports"], maps="awareness (RQ3)"),
 dict(id="D4", sec="D. Safeguards", type="single", text="If you had heard of it: did it change how you use or configure agents?", options=["No", "A little", "Substantially", "I do not use agents"], maps="incident-to-practice link (gap G5)", show_if="D3 is not 'No'"),
 # ---- E. Optional
 dict(id="E1", sec="E. Optional", type="text", text="Optional, one line: is there anything about agents acting without authorization that these questions missed?", maps="item generation for the next version"),
]
META = dict(version="0.1", status="DRAFT - not administered; no responses exist", est_minutes="5-6", required_typing="none (one optional one-line answer)",
            n_items=len(Q), n_closed=sum(q["type"] != "text" for q in Q))
json.dump(dict(meta=META, likert=LIKERT, questions=Q), open("survey/questionnaire.json", "w"), indent=1, ensure_ascii=False)

md = [f"# Practitioner questionnaire on unauthorized actions by AI agents", "",
 f"Version {META['version']} | 17 November 2026 | **{META['status']}**", "",
 "A side instrument to the literature review, not part of its evidence. It asks people who use or build AI agents what they do and expect, so that later versions of the review can compare practice with what the reviewed papers found. See `survey/README.md` for purpose, ethics, analysis plan and growth plan.", "",
 f"{META['n_items']} items, {META['n_closed']} of them closed (single choice, multiple choice, agreement scale, or most/least); about {META['est_minutes']} minutes; no typing required.", "",
 "## Information for participants (first screen)", "",
 "> This short questionnaire is part of a student project at IILM University on how people use AI agents that can take actions, and what can go wrong. It takes about five minutes and almost every question is a single click.",
 ">", "> Taking part is voluntary. You may stop at any time by closing the page, and you may skip any question. We do not ask for your name, e-mail address, employer or any account details, and we do not record your IP address. Answers are stored without identifiers and reported only as totals.",
 ">", "> You must be 18 or older to take part. Contact for questions: **[ name and institute e-mail of the responsible student ]**; supervisor: **[ name ]**.",
 ">", "> ☐ I am 18 or older and I agree to take part. *(required to continue)*", ""]
sec = None
for q in Q:
    if q["sec"] != sec: sec = q["sec"]; md += [f"## {sec}", ""]
    cond = f" *(shown only if {q['show_if']})*" if q.get("show_if") else ""
    md += [f"**{q['id']}.** {q['text']}{cond}", ""]
    if q["type"] in ("single", "multi"):
        box = "○" if q["type"] == "single" else "☐"
        md += [f"- {box} {o}" for o in q["options"]] + [""]
    elif q["type"] == "bestworst":
        md += ["| Most | | Least |", "|:---:|---|:---:|"] + [f"| ○ | {v} | ○ |" for v in q["items"].values()] + ["", "*Choose exactly one in each column.*", ""]
    elif q["type"] == "likert":
        md += ["| | " + " | ".join(q["scale"]) + " |", "|---|" + ":---:|" * len(q["scale"])] + [f"| {v} |" + " ○ |" * len(q["scale"]) for v in q["items"].values()] + [""]
    else: md += ["`____________________________________________` *(optional)*", ""]
md += ["## Closing screen", "", "> Thank you. Your answers have been recorded without any identifying information.", "",
 "## Item map (not shown to participants)", "", "| Item | Type | What it measures, and the review question, gap or finding it relates to |", "|---|---|---|"]
md += [f"| {q['id']} | {q['type']} | {q['maps']} |" for q in Q]
md += ["", "Category letters, gap numbers (G1–G5) and finding numbers (F1–F6) refer to Sections III, V.E and VI of the review.", ""]
open("survey/QUESTIONNAIRE.md", "w").write("\n".join(md))
print(META)
