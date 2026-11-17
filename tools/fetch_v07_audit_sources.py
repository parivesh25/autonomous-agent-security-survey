"""Re-fetch pinned public evidence for the numeric string-presence audit."""
import json,pathlib,requests,subprocess,concurrent.futures
from bs4 import BeautifulSoup
base=pathlib.Path('evidence'); (base/'fulltext').mkdir(exist_ok=True); (base/'incident').mkdir(exist_ok=True)
tmp=pathlib.Path('/tmp/v07_sources');tmp.mkdir(exist_ok=True)
def fetch_pdf(e):
    version=e['version_read'];p=tmp/(version+'.pdf')
    try:
        r=requests.get('https://arxiv.org/pdf/'+version,timeout=60);r.raise_for_status();p.write_bytes(r.content)
        subprocess.run(['pdftotext',str(p),str(base/'fulltext'/(version+'.txt'))],check=True)
        return 'FETCHED '+version
    except Exception as exc:return 'FETCH_FAIL '+version+' '+str(exc)
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    for result in pool.map(fetch_pdf,json.load(open('extraction_matrix.json'))): print(result,flush=True)
incident={
 'hf_disclosure.txt':'https://huggingface.co/blog/security-incident-july-2026',
 'hf_timeline.txt':'https://huggingface.co/blog/agent-intrusion-technical-timeline',
 'metr_2025.txt':'https://metr.org/blog/2025-06-05-recent-reward-hacking/',
 'openai_post.txt':'https://openai.com/index/hugging-face-incident-and-the-road-ahead/',
 'metr_2026.txt':'https://metr.org/blog/2026-08-26-openai-hugging-face-incident-investigation/'}
for name,url in incident.items():
    try:
        r=requests.get(url,headers={'User-Agent':'Mozilla/5.0 research audit'},timeout=60);r.raise_for_status()
        (base/'incident'/name).write_text(BeautifulSoup(r.text,'html.parser').get_text('\n'),encoding='utf-8')
        print('FETCHED',name,flush=True)
    except Exception as exc:print('FETCH_FAIL',name,str(exc),flush=True)
