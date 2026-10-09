#!/usr/bin/env python3
"""Check rendered item coverage, source links and accessible panel associations."""
import json
from html.parser import HTMLParser
from html import escape
from pathlib import Path
from render_impact import ROOT, render

class Page(HTMLParser):
    def __init__(self):
        super().__init__(); self.ids={}; self.items=[]; self.triggers=[]; self.panels=[]; self.links=[]
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if 'id' in a:
            assert a['id'] not in self.ids, f'Duplicate id: {a["id"]}'
            self.ids[a['id']]=a
        if tag=='details' and a.get('class')=='history-item': self.items.append(a)
        if tag=='summary' and 'aria-controls' in a: self.triggers.append(a)
        if a.get('class')=='history-panel': self.panels.append(a)
        if tag=='a': self.links.append(a.get('href'))

d=json.loads((ROOT/'data/impact-history.json').read_text())
assert (ROOT/'content/impact.org').read_text()==render(d)
html=(ROOT/'public/impact/index.html').read_text()
p=Page(); p.feed(html)
assert len(p.items)==len(p.triggers)==len(p.panels)==47
assert {i['id'] for i in p.items}=={i['id'] for i in d['items']}
for item in d['items']:
    ident=item['id'];trigger=p.ids['trigger-'+ident];panel=p.ids['panel-'+ident]
    assert trigger['aria-controls']==panel['id']
    assert panel['aria-labelledby']==trigger['id'] and panel['role']=='region'
    assert all(d['sources'][s]['url'] in p.links for s in item['sources'])
assert 'fm-history-descriptions' not in html
for phrase in ['Not established', 'Evidence limit:', 'Attribution limits', 'Sources reviewed', 'State of the Art FM', '2000s-relational-abstraction', 'DPRIVE']:
    assert phrase.casefold() not in html.casefold(), phrase
for item in d['items']:
    if item['gap']: assert escape(item['gap']) not in html
    if not item['sri_contributors']:
        panel=html.split('id="panel-'+item['id']+'"',1)[1].split('</details>',1)[0]
        assert 'SRI contributors:' not in panel
assert p.ids['trigger-2000s-hybridsal']['aria-controls']=='panel-2000s-hybridsal'
assert 'Bitvector solving</summary>' in html
print('PASS: 47 rendered contributions, 47 trigger/panel associations, all mapped references, no detached decade descriptions.')
