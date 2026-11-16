#!/usr/bin/env python3
"""Minimal HTML -> text (headings marked) for reading saved pages. Usage: html2text.py file.html"""
import sys, re, html
from html.parser import HTMLParser
class P(HTMLParser):
    def __init__(s):
        super().__init__(); s.out=[]; s.skip=0
    def handle_starttag(s,t,a):
        if t in("script","style","nav","svg","noscript","footer","header","button","form"): s.skip+=1
        elif t in("h1","h2","h3","h4","h5","h6"): s.out.append("\n\n"+"#"*int(t[1])+" ")
        elif t in("p","li","tr","div","section","br","figcaption","blockquote","table","dt","dd"): s.out.append("\n")
        elif t in("td","th"): s.out.append(" | ")
    def handle_endtag(s,t):
        if t in("script","style","nav","svg","noscript","footer","header","button","form"): s.skip=max(0,s.skip-1)
    def handle_data(s,d):
        if not s.skip: s.out.append(d)
def convert(raw):
    p=P(); p.feed(raw); t="".join(p.out)
    t=re.sub(r"[ \t\xa0]+"," ",t); t=re.sub(r"\n\s*\n+","\n\n",t)
    return t.strip()
if __name__=="__main__":
    print(convert(open(sys.argv[1],encoding="utf-8",errors="replace").read()))
