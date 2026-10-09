#!/usr/bin/env python3
"""Render the reviewed bibliography into Org; --check detects stale output."""
import argparse
import json
from pathlib import Path
import re
import html
from bibliography import bibtex, citation_key
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
CATEGORIES = ('Slides', 'Technical Reports', 'Journal Articles', 'Conference Papers',
              'Preprints and Working Papers', 'Book Chapters', 'Manuals', 'Books', 'Theses')

def slug(text):
    return re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')

def heading(text, level=1, anchor=None):
    return ['*' * level + ' ' + text, ':PROPERTIES:',
            ':CUSTOM_ID: ' + (anchor or slug(text)), ':END:', '']

def validate(records):
    seen = set()
    keys = set()
    for record in records:
        key = citation_key(record)
        assert re.fullmatch(r'[a-zA-Z0-9][a-zA-Z0-9_-]*', key), key
        assert key not in keys, 'Duplicate citation key: ' + key
        keys.add(key)
        assert record['category'] in CATEGORIES, record['title']
        assert isinstance(record['year'], int) and 1900 <= record['year'] <= 2026
        assert record['title'] and record['authors'] and all(record['authors'])
        assert record['sources'], record['title']
        if record['category'] == 'Conference Papers':
            assert record['venue'] and record['venue_group'], record['title']
        key = (slug(record['title']), record['category'], record['venue_group'])
        assert key not in seen, 'Duplicate publication: ' + record['title']
        seen.add(key)
        for url in [record['url'], *record['sources'], *(x[1] for x in record['links'])]:
            parsed = urlparse(url)
            assert parsed.scheme in ('http', 'https') and parsed.netloc and not re.search(r'\s', url), url
        assert not any(token in json.dumps(record, ensure_ascii=False) for token in ('�', '', 'L0@'))

def entry(record):
    title = record['title']
    authors = ', '.join(record['authors'])
    citation = record['report_number'] or record['venue']
    if record['category'] == 'Preprints and Working Papers':
        citation = 'Unpublished working paper'
    types = {'Technical Reports': 'Technical report', 'Journal Articles': 'Journal article',
             'Conference Papers': 'Conference paper', 'Preprints and Working Papers': 'Preprint / working paper',
             'Book Chapters': 'Book chapter', 'Manuals': 'Manual', 'Slides': 'Slides',
             'Books': 'Book', 'Theses': 'Dissertation'}
    bits = [authors.rstrip('.'), citation.rstrip('.'), types[record['category']]]
    text = '- *[[' + record['url'] + '][' + title + ']]* ' + chr(92) * 2 + '\n  ' + '. '.join(x for x in bits if x) + '.'
    links = []; used = {record['url']}
    for label, url in record['links']:
        if url not in used:
            links.append('[[' + url + '][' + label + ']]'); used.add(url)
    if links:
        text += ' ' + ' · '.join(links) + '.'
    if record['note']:
        text += '\n  ' + record['note']
    key = citation_key(record)
    citation = html.escape(bibtex(record))
    text += ('\n\n  #+begin_export html\n'
             f'  <details class="citation-details" id="bib-{key}">\n'
             f'  <summary aria-label="BibTeX for {html.escape(title, quote=True)}">BibTeX</summary>\n'
             f'  <a href="/bib/{key}.bib" download>Download this citation</a>\n'
             f'  <pre tabindex="0" aria-label="BibTeX citation"><code>{citation}</code></pre>\n'
             '  </details>\n  #+end_export')
    return [text, '']

def render(records):
    years = sorted({r['year'] for r in records}, reverse=True)
    lines = ['#+TITLE: Publications', '#+HTML_CONTENT_CLASS: publications-page',
             '#+DESCRIPTION: SRI formal methods and dependable systems publications, arranged by year.',
             '#+OPTIONS: H:4',
             '# Generated from data/publications.json by scripts/render_publications.py.', '',
             'Research from SRI’s Formal Methods and Dependable Systems program and its predecessors,',
             'including work with collaborators. All publications are arranged by year, newest first,',
             'and alphabetically by title within each year. Distinct conference and journal versions',
             'are retained; preprints of published papers are linked with their published record.',
             'Conference years refer to the meeting, which can precede the proceedings.', '',
             '[[/bib/publications.bib][Download all citations (BibTeX)]]. Each entry also has its own copyable citation and download.', '',
             ' · '.join('[[#year-' + str(y) + '][' + str(y) + ']]' for y in years), '',
             '[[#coverage][Coverage and sources]]', '']
    for year in years:
        lines += heading(str(year), anchor='year-' + str(year))
        for row in sorted((r for r in records if r['year'] == year), key=lambda r: r['title'].casefold()):
            lines += entry(row)
    lines += heading('Coverage and sources', anchor='coverage')
    lines += [f'This bibliography contains {len(records)} records, including dated slides.',
              'It brings together the [[https://www.csl.sri.com/papers/][CSL paper archive]],',
              '[[https://www.csl.sri.com/programs/formalmethods/][Formal Methods program archive]],',
              '[[https://www.csl.sri.com/~rushby/biblio.html][John Rushby’s bibliography]],',
              '[[https://www.csl.sri.com/~rushby/pvs-bib.html][historical PVS bibliography]],',
              '[[https://www.csl.sri.com/users/shankar/shankar-papers.html][Natarajan Shankar’s papers]],',
              '[[https://www.csl.sri.com/users/tiwari/][Ashish Tiwari’s publications]],',
              '[[https://www.csl.sri.com/users/sgl/Work/][Stéphane Graham-Lengrand’s publications]],',
              '[[https://yices.csl.sri.com/yices2-documentation.html][Yices documentation]],',
              '[[https://www.csl.sri.com/~neumann/references.html][Peter G. Neumann’s selected publication history]],',
              'his [[https://www.csl.sri.com/~neumann/][SRI homepage]] and [[https://www.csl.sri.com/people/neumann/][CSL paper list]],',
              'and the Cambridge [[https://www.cl.cam.ac.uk/research/security/ctsrd/publications.html][CTSRD / CHERI publication inventory]]',
              'and [[https://www.cl.cam.ac.uk/research/security/ctsrd/cheri/cheriformal_bib.html][CHERI formal-methods bibliography]], with publisher',
              'and arXiv records used to resolve recent publication status and conflicting metadata.', '',
              'Coverage is substantial but not exhaustive. Some legacy records lack dates, complete',
              'citations, or accessible files; some links lead to an author bibliography rather than a',
              'dedicated paper page. External researchers’ use of SRI tools alone does not establish',
              'SRI authorship. Undated records are omitted. The CAV author audit also includes three',
              'papers from Harald Ruess’s wider publication history, visibly marked as having no SRI affiliation.',
              'Legacy report identifiers retained from the earlier program page are noted where their',
              'dates differ from the available version. Archive links may offer PostScript instead of PDF.', '',
              'The Neumann reconciliation starts with his SRI period (September 1971 onward).',
              'It includes research papers, reports, books and chapters, and selected substantive essays;',
              'routine RISKS digests, serial columns, interviews, testimony and undated material are excluded.',
              'Committee books identify institutional authors and his committee contribution.',
              'CHERI / CTSRD entries require at least one direct SRI author at the time of publication;',
              'project collaboration, funding, and affiliation with an external partner alone do not qualify.',
              'Qualifying joint papers and separately numbered reports are retained. This is coverage of the linked source',
              'inventories, not a claim to include every CHERI-related publication worldwide.',
              'Forthcoming work, draft versions, and historical citations without original full text are marked.', '',
              'Metadata reviewed October 9, 2026.']
    return '\n'.join(lines) + '\n'

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    records = json.loads((ROOT / 'data/publications.json').read_text())
    validate(records)
    output = render(records)
    exports = {ROOT / 'static/bib' / (citation_key(r) + '.bib'): bibtex(r) for r in records}
    exports[ROOT / 'static/bib/publications.bib'] = '\n'.join(bibtex(r) for r in sorted(records, key=citation_key))
    target = ROOT / 'content/pubs.org'
    if args.check:
        if target.read_text() != output:
            raise SystemExit('content/pubs.org is stale; run python3 scripts/render_publications.py')
        assert set((ROOT / 'static/bib').glob('*.bib')) == set(exports), 'Unexpected or missing BibTeX files'
        for path, content in exports.items():
            assert path.exists() and path.read_text() == content, 'Stale BibTeX: ' + str(path)
    else:
        target.write_text(output)
        (ROOT / 'static/bib').mkdir(exist_ok=True)
        for stale in set((ROOT / 'static/bib').glob('*.bib')) - set(exports):
            stale.unlink()
        for path, content in exports.items():
            path.write_text(content)
    print(f'Validated {len(records)} publication records; ' + ('Org output is current.' if args.check else 'rendered content/pubs.org.'))
