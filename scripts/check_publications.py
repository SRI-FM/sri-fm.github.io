#!/usr/bin/env python3
"""Check generated citations with BibTeX itself and the built HTML with HTMLParser."""
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
from html.parser import HTMLParser
from bibliography import bibtex, citation_key, escape
from render_publications import validate, ROOT

records = json.loads((ROOT / 'data/publications.json').read_text())
validate(records)
expected = {citation_key(r): bibtex(r) for r in records}
assert escape('PVS & C_1 {x} 50% # $ \\ ~ ^') == r'PVS \& C\_1 \{x\} 50\% \# \$ \textbackslash{} \textasciitilde{} \textasciicircum{}'
assert len(expected) == len(records)
audit = json.loads((ROOT / 'data/cheri-sri-affiliation-audit-2026-10-09.json').read_text())
for decision in audit['decisions']:
    key = decision['citation_key']
    assert (key in expected) == (decision['decision'] == 'retain'), decision['title']
    if key in expected:
        record = next(r for r in records if citation_key(r) == key)
        assert record['sri_authorship']['author'] in record['authors']
        assert record['sri_authorship']['evidence']
assert {p.name for p in (ROOT / 'public/bib').glob('*.bib')} == {k + '.bib' for k in expected} | {'publications.bib'}, 'Orphaned published citations'
for key, text in expected.items():
    assert (ROOT / 'static/bib' / (key + '.bib')).read_text() == text

# A real BibTeX parser plus its name formatter catches syntax and malformed names.
exe = shutil.which('bibtex')
if not exe:
    candidate = Path('/usr/local/texlive/2025/bin/universal-darwin/bibtex')
    exe = str(candidate) if candidate.is_file() else None
if not exe:
    raise SystemExit('Install BibTeX (TeX Live) to run the parser validation.')
style = r'''ENTRY { author title year } {} {}
INTEGERS { i n }
FUNCTION {article} {}
FUNCTION {inproceedings} {}
FUNCTION {techreport} {}
FUNCTION {incollection} {}
FUNCTION {book} {}
FUNCTION {manual} {}
FUNCTION {phdthesis} {}
FUNCTION {misc} {}
FUNCTION {unpublished} {}
FUNCTION {check.entry} {
  cite$ write$ newline$
  author num.names$ 'n := #1 'i :=
  { i n #1 + < }
  { author i "{ff }{vv }{ll}{, jj}" format.name$ pop$ i #1 + 'i := }
  while$
}
READ
ITERATE {check.entry}
'''
with tempfile.TemporaryDirectory(prefix='sri-bibtex-') as tmp:
    tmp = Path(tmp)
    (tmp / 'check.bst').write_text(style)
    (tmp / 'all.bib').write_text((ROOT / 'static/bib/publications.bib').read_text())
    (tmp / 'check.aux').write_text('\\relax\n\\citation{*}\n\\bibstyle{check}\n\\bibdata{all}\n')
    result = subprocess.run([exe, 'check'], cwd=tmp, capture_output=True, text=True)
    assert result.returncode == 0, result.stdout + result.stderr
    parsed = (tmp / 'check.bbl').read_text().splitlines()
    assert len(parsed) == len(expected) and set(parsed) == set(expected)

class Citations(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids = []; self.citations = {}; self.key = None
        self.in_code = False; self.text = ''; self.downloads = []; self.stack = []
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs: self.ids.append(attrs['id'])
        if tag == 'details' and attrs.get('class') == 'citation-details':
            assert 'li' in self.stack, 'Citation detached from its publication list item'
            assert 'open' not in attrs, 'Citation must start collapsed'
            self.key = attrs['id'].removeprefix('bib-')
        if tag == 'a' and 'download' in attrs: self.downloads.append(attrs['href'])
        if self.key and tag == 'code': self.in_code = True; self.text = ''
        if tag not in ['br','hr','img','input','meta','link','source','wbr']: self.stack.append(tag)
    def handle_data(self, text):
        if self.in_code: self.text += text
    def handle_endtag(self, tag):
        if tag == 'code' and self.in_code:
            self.citations[self.key] = self.text; self.in_code = False
        if tag == 'details': self.key = None
        if tag in self.stack:
            self.stack = self.stack[:len(self.stack)-1-self.stack[::-1].index(tag)]

page = Citations(); page.feed((ROOT / 'public/pubs/index.html').read_text())
assert len(page.ids) == len(set(page.ids)), 'Duplicate HTML IDs'
assert page.citations == expected, 'Rendered citation text differs from the download'
assert set(page.downloads) == {'/bib/' + k + '.bib' for k in expected}
assert len(page.downloads) == len(expected)
for href in page.downloads + ['/bib/publications.bib']:
    assert (ROOT / 'public' / href.lstrip('/')).read_bytes() == (ROOT / 'static' / href.lstrip('/')).read_bytes()
print(f'PASS: {len(records)} records, unique keys, parsed BibTeX author lists, matching collapsed HTML citations, and published downloads.')
