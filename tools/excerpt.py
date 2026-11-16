#!/usr/bin/env python3
"""Print a reading view of a saved full text: heading outline, then the opening of sections
whose headings match the given patterns. Usage: excerpt.py file [chars_per_section] [regex]"""
import sys, re
t=open(sys.argv[1],errors="replace").read()
lim=int(sys.argv[2]) if len(sys.argv)>2 else 1500
pat=re.compile(sys.argv[3] if len(sys.argv)>3 else r"method|setup|setting|threat|design|environment|benchmark|evaluat|experiment|result|finding|limitation|discussion|conclusion|protocol|attack|defen", re.I)
i=t.find("References\n"); j=t.rfind("\n## References"); 
parts=re.split(r"\n(?=#{2,4} )", t)
print("OUTLINE:", " / ".join(p.split("\n",1)[0].strip("# ").strip()[:45] for p in parts[1:] if p.split("\n",1)[0].strip("# ").strip())[:1800])
seen=0
for p in parts[1:]:
    h,_,b=p.partition("\n"); h=h.strip("# ").strip()
    if re.match(r"references|acknowledg|appendix|[A-Z]\.?\d* |impact statement|ethic", h, re.I) and seen>3: 
        if re.match(r"references", h, re.I): break
        continue
    b=re.sub(r"\n\s*\n+","\n",b).strip()
    if h and pat.search(h) and len(b)>200:
        seen+=1; print(f"\n--- [{h[:80]}] ({len(b)} chars)\n{b[:lim]}")
