"""Check the canonical v0.7 source and, when built, its PDF page boundaries."""
import re,json,subprocess,hashlib
from pathlib import Path
p=Path('paper/latex_v0.7')
s=(p/'manuscript.tex').read_text(encoding='utf-8')
r=(p/'references.tex').read_text(encoding='utf-8')
refs=re.findall(r'\\bibitem\{(r\d+)\}',r)
cites=re.findall(r'\\cite\{(r\d+)\}',s)
assert len(refs)==len(set(refs))==40
assert set(cites)==set(refs)
assert s.count('\\begin{longtable}')==11
assert s.count('\\begin{figure}')==3
assert s.count('\\section{')==8
abstract=s.split('\\textbf{Abstract—}')[1].split('\n')[0]
assert 150<=len(abstract.split())<=250
assert '15 of 35' in s
assert '89\\%' in s and '17\\%' in s
assert 'abhishek.pandey@iilm.edu' in (p/'cover.tex').read_text(encoding='utf-8')
cover=(p/'cover.tex').read_text(encoding='utf-8')
assert 'Name & Dr. Abhishek Pandey' in cover and 'Sharma' not in cover and 'Sharma' not in s, 'supervisor name must match the user-confirmed Dr. Abhishek Pandey'
assert 'Marks)' in cover and '\\_\\_\\_ Marks' in cover, 'assessment marks must stay blank'
assert '___' not in (p/'cover.tex').read_text(encoding='utf-8') # escaped underscores only
print('PASS canonical LaTeX: 40 resolved references, 11 tables, 3 figures, 8 sections')
print('PASS abstract length:',len(abstract.split()),'words')
print('PASS retained corrected F6 and W021 figures; supervisor Dr. Abhishek Pandey with confirmed email; marks blank')
pdf=Path('paper/AgentSecuritySurvey_v0.7.pdf')
if pdf.exists():
    info=subprocess.check_output(['pdfinfo',str(pdf)],text=True)
    total=int(re.search(r'^Pages:\s+(\d+)',info,re.M)[1])
    pages=[subprocess.check_output(['pdftotext','-f',str(i),'-l',str(i),str(pdf),'-'],text=True,encoding='utf-8') for i in range(1,total+1)]
    start=[i+1 for i,t in enumerate(pages) if 'Abstract—' in t]
    annex=[i+1 for i,t in enumerate(pages) if 'ANNEXURE: SEARCH LOG' in t]
    assert len(start)==len(annex)==1,(start,annex)
    n=annex[0]-start[0]
    assert n<=12, f'{n} paper pages exceeds 12'
    assert start==[2],f'Cover must be one page: paper starts {start}'
    print(f'PASS PDF: {total} total pages; paper {start[0]}–{annex[0]-1} = {n} pages; annex starts {annex[0]}')
    log=(p/'main.log').read_text(errors='replace')
    assert not re.search(r'LaTeX Warning: (?:Reference|Citation).*undefined',log)
    assert 'Missing character:' not in log
    print('PASS no undefined references or missing glyphs')
    print('Overfull boxes (inspect visually):',len(re.findall('Overfull',log)))
    print('PDF SHA256:',hashlib.sha256(pdf.read_bytes()).hexdigest())
