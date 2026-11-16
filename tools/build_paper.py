#!/usr/bin/env python3
"""Assemble the manuscript: MANUSCRIPT.md, three figures, and the DOCX from the professor's template.
Run from the repo root after tools/build_t02.py:  python3 tools/build_paper.py"""
import json, re, sys, copy, calendar
sys.path.insert(0, "paper")
import content as C, extraction_data as X
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import docx
from docx.shared import Cm
from docx.oxml.ns import qn
from docx.text.paragraph import Paragraph
from docx.table import Table

N = json.load(open("paper/counts.json"))
works = {w["identifiers"]["arxiv"]: w for w in json.load(open("works.json"))}
EX = {e["key"]: e for e in X.E}
OUT_DOCX, OUT_MD = "paper/AgentSecuritySurvey_draft_v0.2.docx", "MANUSCRIPT.md"
ROMAN = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X"]

# ---------- references
def surname(n): return n.split()[-1] if not n.endswith("de Witt") else "Schroeder de Witt"
def initials(n):
    parts = n.split(); sn = surname(n); given = n[: len(n) - len(sn)].split()
    return " ".join(p[0] + "." for p in given) + " " + sn
def auphrase(k):
    a = works[EX[k]["arxiv"]]["authors"]
    return surname(a[0]) if len(a) == 1 else f"{surname(a[0])} and {surname(a[1])}" if len(a) == 2 else f"{surname(a[0])} et al."
def refentry(k):
    if k in X.INCIDENT_SOURCES:
        s = X.INCIDENT_SOURCES[k]; who = s.get("authors", s["publisher"])
        d = s["published"]; pub = f"{calendar.month_abbr[int(d[5:7])]}. {int(d[8:])}, {d[:4]}"
        return f"{who}, “{s['title']},” {s['publisher']}, {pub}. [Online]. Available: {s['url']}. [Accessed: 16 Nov 2026]."
    w = works[EX[k]["arxiv"]]; a = w["authors"]
    names = initials(a[0]) + " et al." if len(a) > 6 else (", ".join(initials(x) for x in a[:-1]) + (", and " if len(a) > 2 else " and ") + initials(a[-1]) if len(a) > 1 else initials(a[0]))
    d = w["version_date"]; mon = calendar.month_abbr[int(d[5:7])] + "." if int(d[5:7]) != 5 else "May"
    extra = " Also in Proc. 16th ACM Workshop Artif. Intell. Secur. (AISec), 2023, doi: 10.1145/3605764.3623985." if k == "greshake" else ""
    return f"{names}, “{w['title']},” arXiv preprint arXiv:{w['version_checked']}, {mon} {d[:4]}.{extra}"
ORDER = []
def cite(m):
    k = m.group(1)
    if k not in ORDER: ORDER.append(k)
    return f"[{ORDER.index(k) + 1}]"
def T(s):
    s = s.format_map(type("D", (dict,), {"__missing__": lambda self, k: "{" + k + "}"})(N)) if "{n_" in s else s
    s = re.sub(r"\{au:(\w+)\}", lambda m: auphrase(m.group(1)), s)
    return re.sub(r"\{c:(\w+)\}", cite, s)

# Resolve text in reading order so numbers follow first appearance.
A = dict(abstract=T(C.ABSTRACT), ia=[T(p) for p in C.INTRO_A], ib=T(C.INTRO_B), rq=C.RQS, con=[T(c) for c in C.CONTRIB],
         ma=T(C.METH_A), mc=T(C.METH_C), tax=T(C.TAX_P))
S4 = {}
for cat in "ABCD":
    S4[cat] = dict(title=C.SEC4[cat]["title"], paras=[T(p) for p in C.SEC4[cat]["paras"]])
    S4[cat]["rows"] = [(T("{c:%s}" % r[0]), works[EX[r[0]]["arxiv"]]["first_public_date"][:4], *r[1:]) for r in C.CAT_TABLE[cat]]
    S4[cat]["close"] = T(C.SEC4[cat]["close"])
MASTER = [(T("{c:%s}" % r[0]), works[EX[r[0]]["arxiv"]]["first_public_date"][:4], *r[1:]) for r in C.MASTER]
S5B = [T(p) for p in C.SEC5_B]; T9 = [tuple(T(x) for x in r) for r in C.TABLE_IX]; S5D = T(C.SEC5_D)
GAPS = [tuple(T(x) for x in r) for r in C.GAPS]; GAPP = T(C.GAP_P); FUT = [T(x) for x in C.FUTURE]; CONC = T(C.CONCLUSION)
REFS = [f"[{i + 1}]  {refentry(k)}" for i, k in enumerate(ORDER)]
num = lambda k: ORDER.index(k) + 1
assert set(EX) <= set(ORDER), set(EX) - set(ORDER)

# ---------- figures (print: hue + hatch + direct labels; palette validated with the dataviz script)
COL = {"A": "#2a78d6", "B": "#eb6834", "C": "#1baf7a", "D": "#eda100"}; HATCH = {"A": "", "B": "///", "C": "...", "D": "xx"}
INK, MUTE = "#0b0b0b", "#52514e"
plt.rcParams.update({"font.family": "serif", "font.serif": ["Times New Roman", "Liberation Serif", "DejaVu Serif"], "font.size": 9})
def box(ax, x, y, w, h, text, fc="white", fs=8.5, bold=False):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.06", fc=fc, ec=INK, lw=0.8))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs, color=INK, fontweight="bold" if bold else "normal", linespacing=1.25)
def fig1():
    fig, ax = plt.subplots(figsize=(6.3, 4.6)); ax.set_xlim(0, 10); ax.set_ylim(0, 10); ax.axis("off")
    bs = N["by_search"]
    main = [f"Records identified by the searches (n = {N['n_rec']})\nSciSpace 30; arXiv API 88;\nCrossref (IEEE, ACM, Springer) {bs['D']}; targeted title checks {bs['W']}",
            f"Distinct works with verified metadata (n = {N['n_works']})",
            f"Works screened on title and abstract (n = {N['n_works']})",
            f"Works placed in the reading queue (n = {N['n_queue']})",
            f"Works read in full text and included (n = {N['n_inc']})"]
    side = [f"Removed:\n{N['n_dup']} repeated or duplicate records\n{N['n_unv']} with no primary record", None,
            f"Not queued:\n{N['n_exc']} out of scope\n{N['n_ctx']} context only\n{N['n_res']} eligible, held in reserve\n{N['n_await']} awaiting full text",
            f"Not reached: {N['n_unread']}"]
    ys = [8.0, 6.1, 4.3, 2.5, 0.7]; hs = [1.7, 1.0, 1.0, 1.0, 1.0]
    for i, (t, y, h) in enumerate(zip(main, ys, hs)):
        box(ax, 0.1, y, 6.0, h, t, fc="#eef3fa" if i == 4 else "white", bold=(i == 4), fs=8.5)
        if i < 4:
            ax.annotate("", xy=(3.1, ys[i + 1] + hs[i + 1] + 0.05), xytext=(3.1, y - 0.05), arrowprops=dict(arrowstyle="-|>", color=INK, lw=0.9))
            if side[i]:
                ym = (y + ys[i + 1] + hs[i + 1]) / 2
                ax.annotate("", xy=(6.5, ym), xytext=(3.1, ym), arrowprops=dict(arrowstyle="-|>", color=MUTE, lw=0.8))
                ax.text(6.6, ym, side[i], ha="left", va="center", fontsize=8, color=INK, linespacing=1.25)
    fig.savefig("paper/fig1_selection_flow.png", dpi=300, bbox_inches="tight", facecolor="white"); plt.close(fig)
def fig2():
    leaves = {"A": [("How it arises", ["denison", "chess"]), ("How often it occurs", ["impossible", "evilgenie", "rhb", "nishimura", "huang"]), ("Evaluation audited", ["rha", "hackdetect"])],
              "B": [("Threat and benchmarks", ["greshake", "injecagent", "agentdojo", "asb"]), ("Benchmarks questioned", ["silent", "firewalls", "adaptive", "livepi"]), ("Defence by design", ["camel"])],
              "C": [("Attacks on channels", ["infection", "aitm", "masexec"]), ("Composition tests", ["camelstalk", "macontrol"]), ("System design", ["arch", "delegation"])],
              "D": [("Control protocols", ["aicontrol", "ctrlz", "shade"]), ("Adaptive attackers", ["evalcp", "adaptmon"]), ("Uninstructed behaviour", ["cot", "scheming"])]}
    names = {"A": "A. Objective and\nevaluation integrity", "B": "B. Input and tool\nauthorization", "C": "C. Inter-agent trust\nand communication", "D": "D. Oversight and\ncontrol integrity"}
    fig, ax = plt.subplots(figsize=(6.9, 3.9)); ax.set_xlim(0, 10); ax.set_ylim(0, 10); ax.axis("off")
    box(ax, 2.6, 8.7, 4.8, 1.0, "Security failures in autonomous AI agents\n(grouped by the boundary under test)", fs=8.5, bold=True)
    for i, cat in enumerate("ABCD"):
        x = 0.1 + i * 2.5; cx = x + 1.15
        ax.plot([5, 5, cx, cx], [8.7, 8.2, 8.2, 7.75], color=INK, lw=0.8)
        ax.add_patch(FancyBboxPatch((x, 6.55), 2.3, 1.2, boxstyle="round,pad=0.02,rounding_size=0.06", fc="white", ec=INK, lw=0.8))
        ax.add_patch(plt.Rectangle((x - 0.02, 6.53), 0.16, 1.24, fc=COL[cat], ec=INK, lw=0.4, hatch=HATCH[cat]))
        ax.text(cx + 0.06, 7.15, names[cat], ha="center", va="center", fontsize=8.2, fontweight="bold", color=INK)
        for j, (lab, ks) in enumerate(leaves[cat]):
            y = 4.6 - j * 1.75
            ax.plot([cx, cx], [6.55 if j == 0 else y + 1.75, y + 1.25], color=INK, lw=0.6)
            refs = ", ".join(f"[{n}]" for n in sorted(num(k) for k in ks))
            box(ax, x, y, 2.3, 1.25, f"{lab}\n{refs}", fs=7.6)
    fig.savefig("paper/fig2_taxonomy.png", dpi=300, bbox_inches="tight", facecolor="white"); plt.close(fig)
def fig3():
    yrs = ["2023", "2024", "2025", "2026"]; lab = {"A": "A. Objective and evaluation integrity", "B": "B. Input and tool authorization", "C": "C. Inter-agent trust", "D": "D. Oversight and control"}
    fig, ax = plt.subplots(figsize=(5.0, 3.0)); bottom = [0] * 4
    for cat in "ABCD":
        v = [N["by_year_cat"][y].get(cat, 0) for y in yrs]
        ax.bar(yrs, v, 0.55, bottom=bottom, color=COL[cat], hatch=HATCH[cat], edgecolor="white", linewidth=1.5, label=lab[cat])
        for i, n in enumerate(v):
            if n: ax.text(i, bottom[i] + n / 2, str(n), ha="center", va="center", fontsize=8, color=INK, bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none", alpha=0.9))
        bottom = [b + n for b, n in zip(bottom, v)]
    for i, t in enumerate(bottom): ax.text(i, t + 0.25, f"{t}", ha="center", va="bottom", fontsize=8.5, color=INK, fontweight="bold")
    ax.set_ylabel("Included works (n = %d)" % N["n_inc"]); ax.set_xlabel("Year first made public"); ax.set_ylim(0, max(bottom) + 2)
    ax.yaxis.grid(True, color="#dddddd", lw=0.6); ax.set_axisbelow(True)
    for s in ("top", "right"): ax.spines[s].set_visible(False)
    ax.legend(fontsize=7.5, frameon=False, loc="upper left")
    fig.savefig("paper/fig3_trend.png", dpi=300, bbox_inches="tight", facecolor="white"); plt.close(fig)
fig1(); fig2(); fig3()
by = N["by_year_cat"]
FIG3CAP = f"Fig. 3. Included works by year first made public and by category (n = {N['n_inc']}). Counts describe this review's corpus, not the field."

# ---------- tables as (caption, header, rows)
TABLES = {
 1: ("Sources Searched and Search Strings Used", ["Source", "Search string used", "Date searched", "Hits"], C.TABLE_I),
 2: ("Inclusion and Exclusion Criteria", ["A work was included if", "A work was excluded if"], C.TABLE_II),
 3: ("Categories of the Taxonomy and Where Each Is Reviewed", ["Category", "What the works in it have in common", "Works", "Reviewed in"], C.TABLE_III),
 8: ("Comparison of the Reviewed Works Across Categories", ["Ref.", "Year", "Category", "Approach", "Data or test bed", "Measure used", "Main finding"], [(r[0], r[1], r[2], r[3], r[4], r[5], r[6]) for r in MASTER]),
 9: ("Datasets, Tools and Measures Used in the Reviewed Work", ["Dataset, tool or measure", "Used by", "Why it is used", "Known caveat"], T9),
 10: ("Research Gaps Identified by This Review", ["Gap", "What is missing", "Evidence from the reviewed work"], GAPS),
}
for i, cat in enumerate("ABCD"):
    TABLES[4 + i] = (f"Comparison of the Works Reviewed in {S4[cat]['title']}", ["Ref.", "Year", "Approach used", "Data or test bed", "Reported outcome", "Limitation stated or observed"], S4[cat]["rows"])
cap = lambda n: f"Table {ROMAN[n - 1]}. {TABLES[n][0]}"

# ---------- flow of the paper block: list of (kind, payload)
ORG = "The rest of this paper is organised as follows. Section II describes how the reviewed works were searched for and selected. Section III presents the taxonomy used to group them. Section IV reviews the work category by category. Section V compares the reviewed work and reports the trends observed. Section VI states the research gaps and Section VII the future directions that follow from them. Section VIII concludes the review."
F = [("PaperTitle", C.TITLE),
     ("AuthorBlk!", "[ First Student Name ]¹, [ Second Student Name ]¹, [ Third Student Name ]¹, [ Supervisor Name ]²"), ("AuthorBlk", "¹ B.Tech Student, ² Faculty Supervisor"),
     ("AuthorBlk", "School of Computer Science and Engineering, IILM University, Gurugram, Haryana, India"), ("AuthorBlk!", "[ name1@iilm.edu ], [ name2@iilm.edu ], [ supervisor@iilm.edu ]"),
     ("AbsHead", ("Abstract—", A["abstract"])), ("AbsHead", ("Keywords: ", C.KEYWORDS)),
     ("H1", "I. Introduction"), ("H2", "A. Background"), *[("Body", p) for p in A["ia"]], ("H2", "B. Why this review is needed"), ("Body", A["ib"]),
     ("H2", "C. Review questions"), *[("Body", p) for p in A["rq"]], ("H2", "D. Contributions of this review"), *[("Body", p) for p in A["con"]],
     ("H2", "E. Organisation of the paper"), ("Body", ORG),
     ("H1", "II. Review Methodology"), ("H2", "A. Sources searched and search strings"), ("Body", A["ma"]), ("table", 1),
     ("H2", "B. Inclusion and exclusion criteria"), ("table", 2), ("H2", "C. Selection process"), ("fig", ("paper/fig1_selection_flow.png", 14.5, "Fig. 1. Flow of the selection process, from works identified to works included.")), ("Body", A["mc"]),
     ("H1", "III. Taxonomy of the Reviewed Work"), ("Body", A["tax"]), ("fig", ("paper/fig2_taxonomy.png", 15.5, "Fig. 2. Taxonomy of the reviewed work, with the included works on the leaves.")), ("table", 3),
     ("H1", "IV. Review of the Literature")]
for i, cat in enumerate("ABCD"):
    F += [("H2", f"{cat}. {S4[cat]['title']}"), *[("Body", p) for p in S4[cat]["paras"]], ("table", 4 + i), ("Body", S4[cat]["close"])]
F += [("H1", "V. Comparative Analysis and Discussion"), ("H2", "A. Comparison across categories"),
      ("Body", "Table VIII places fifteen of the included works side by side; the full extraction for all of them is in the evidence repository."), ("table", 8),
      ("H2", "B. Trends observed"), ("fig", ("paper/fig3_trend.png", 11.5, FIG3CAP)), *[("Body", p) for p in S5B],
      ("H2", "C. Datasets, tools and measures in common use"), ("Body", "Table IX lists the test beds and measures that recur across the included works, with the caveat that most affects comparison."), ("table", 9),
      ("H2", "D. Reading the motivating incident against the reviewed work"), ("Body", S5D),
      ("H1", "VI. Research Gaps and Open Challenges"), ("Body", "Table X states five gaps with the works that support each and the works that partly answer it."), ("table", 10), ("Body", GAPP),
      ("H1", "VII. Future Directions"), *[("Body", x) for x in FUT], ("H1", "VIII. Conclusion"), ("Body", CONC),
      ("H1", "Acknowledgment"), ("Fill", C.ACK), ("H1", "References"), *[("RefItem", r) for r in REFS]]

# ---------- Markdown
md = [f"# {C.TITLE}", "", "Draft v0.2 | 16 November 2026 | Reading and drafting by an AI assistant; human reading, checking and authorship details pending (see handoffs/claude-t02-20261116-001.md).", ""]
for kind, p in F[1:]:
    if kind == "H1": md += ["", f"## {p}", ""]
    elif kind == "H2": md += ["", f"### {p}", ""]
    elif kind == "AbsHead": md += [f"**{p[0]}**{p[1]}", ""]
    elif kind == "table":
        c, h, rows = TABLES[p]; md += ["", f"**{cap(p).upper()}**", "", "| " + " | ".join(h) + " |", "|" + "---|" * len(h)] + ["| " + " | ".join(str(x) for x in r) + " |" for r in rows] + [""]
    elif kind == "fig": md += ["", f"![{p[2]}]({p[0]})", "", f"*{p[2]}*", ""]
    elif kind == "RefItem": md += [p, ""]
    else: md += [p, ""]
open(OUT_MD, "w").write("\n".join(md))

# ---------- DOCX from the template
d = docx.Document("template/IILM_Survey_Paper_Template.docx"); body = d.element.body; els = list(body)
def style_of(el):
    pPr = el.find(qn("w:pPr")); ps = pPr.find(qn("w:pStyle")) if pPr is not None else None
    return ps.get(qn("w:val")) if ps is not None else None
proto = {}
for el in els:
    if el.tag == qn("w:p") and style_of(el) and style_of(el) not in proto and "".join(t.text or "" for t in el.iter(qn("w:t"))).strip(): proto[style_of(el)] = copy.deepcopy(el)
tproto = {len(Table(els[i], d).columns): copy.deepcopy(els[i]) for i in (123, 173, 119, 141, 160)}   # 2,3,4,6,7 columns
tspecial = {1: copy.deepcopy(els[119]), 3: copy.deepcopy(els[134]), 9: copy.deepcopy(els[168])}
blank = copy.deepcopy(els[126])                                 # a Normal paragraph near Fig. 1
def set_text(p_el, text, keep_red=False):
    runs = p_el.findall(qn("w:r"))
    for r in runs[1:]: p_el.remove(r)
    r = runs[0]; 
    for t in r.findall(qn("w:t"))[1:]: r.remove(t)
    for x in list(r):
        if x.tag in (qn("w:br"), qn("w:tab")): r.remove(x)
    t = r.find(qn("w:t"))
    if t is None:
        from docx.oxml import OxmlElement
        t = OxmlElement("w:t"); r.append(t)
    t.text = text; t.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
    if not keep_red:
        rpr = r.find(qn("w:rPr"))
        if rpr is not None:
            for c in rpr.findall(qn("w:color")) + rpr.findall(qn("w:highlight")): rpr.remove(c)
def newp(style, text, keep_red=False):
    el = copy.deepcopy(proto[style]); set_text(el, text, keep_red); return el
def abs_p(label, text):
    el = copy.deepcopy(proto["AbsHead"]); runs = el.findall(qn("w:r"))
    for r in runs[2:]: el.remove(r)
    for r, s in zip(runs[:2], (label, text)):
        r.find(qn("w:t")).text = s; r.find(qn("w:t")).set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
        rpr = r.find(qn("w:rPr"))
        if rpr is not None:
            for c in rpr.findall(qn("w:color")): rpr.remove(c)
    return el
def cell_set(tc, text):
    ps = tc.findall(qn("w:p"))
    for p in ps[1:]: tc.remove(p)
    p = ps[0]
    if not p.findall(qn("w:r")):
        Paragraph(p, None).add_run("")
    set_text(p, str(text))
def newtable(n):
    c, h, rows = TABLES[n]; tbl = copy.deepcopy(tspecial.get(n, tproto[len(h)])); trs = tbl.findall(qn("w:tr"))
    for tr in trs[2:]: tbl.remove(tr)
    for tc, x in zip(trs[0].findall(qn("w:tc")), h): cell_set(tc, x)
    rowp = trs[1]; tbl.remove(rowp)
    for r in rows:
        tr = copy.deepcopy(rowp)
        for tc, x in zip(tr.findall(qn("w:tc")), r): cell_set(tc, x)
        tbl.append(tr)
    return tbl
# drop Block B (guidance), the paper-block placeholders, and every blue Note
anchor = els[198]
for i, el in enumerate(els):
    if 24 <= i <= 86 or 88 <= i <= 197 or (el.tag == qn("w:p") and style_of(el) == "Note"): body.remove(el)
for kind, p in F:
    if kind == "table":
        anchor.addprevious(newp("TblCap", cap(p))); anchor.addprevious(newtable(p))
    elif kind == "fig":
        el = copy.deepcopy(blank)
        for r in el.findall(qn("w:r")): el.remove(r)
        ppr = el.find(qn("w:pPr"))
        if ppr is not None:
            for x in ppr.findall(qn("w:pBdr")) + ppr.findall(qn("w:shd")): ppr.remove(x)
        anchor.addprevious(el); para = Paragraph(el, d._body); para.alignment = 1; para.add_run().add_picture(p[0], width=Cm(p[1]))
        anchor.addprevious(newp("FigCap", p[2]))
    elif kind == "AbsHead": anchor.addprevious(abs_p(*p))
    elif kind.endswith("!"): anchor.addprevious(newp(kind[:-1], p, keep_red=True))
    elif kind == "Fill": anchor.addprevious(newp("Fill", p, keep_red=True))
    else: anchor.addprevious(newp(kind, p))
# cover and annexure: fill only what the ledgers establish; leave personal/course placeholders red
REPO = "https://github.com/parivesh25/autonomous-agent-security-survey"
def fill_para(match, text, keep_red=False):
    for p in d.paragraphs:
        if match in p.text: set_text(p._p, text, keep_red); return
fill_para("[ TITLE OF THE SURVEY ]", C.TITLE); fill_para("[ https://github.com/<organisation-or-user>/<repository> ]", REPO)
for t in d.tables:
    for row in t.rows:
        k = row.cells[0].text.strip()
        v = {"Works reviewed": f"{N['n_inc']} papers, first made public between 2023 and 2026",
             "Sources searched": "SciSpace, arXiv, Crossref (IEEE, ACM and Springer records), targeted title checks",
             "Repository URL": REPO, "Literature matrix file": "literature_matrix.json (one row per record), works.json (one per work), extraction_matrix.json (one per work read)",
             "Reference library export": "references_candidates.bib", "Search log file": "search_log.json",
             "Works identified, screened and included": f"{N['n_rec']} records identified, {N['n_works']} works screened, {N['n_inc']} included"}.get(k)
        if v: cell_set(row.cells[1]._tc, v)
fill_para("Use of AI tools:", "Use of AI tools: [ DRAFT FOR THE TEAM TO CONFIRM OR CORRECT. ChatGPT with SciSpace was used for the pilot search. Claude (Anthropic) was used to verify metadata at arXiv and Crossref, run further searches, screen abstracts, read the full text of the 32 included works, extract the matrix, and draft this paper. As of 16 November 2026 no team member has yet confirmed reading any included work; the declaration above must not be signed until each member has read the works in their categories and checked the numbers quoted from them. ]", keep_red=True)
d.save(OUT_DOCX)
words = sum(len(p.split()) for k, p in F if k in ("Body",)) + len(A["abstract"].split())
print("refs", len(REFS), "| body+abstract words", words, "| table words", sum(len(" ".join(map(str, r)).split()) for n in TABLES for r in TABLES[n][2]))
