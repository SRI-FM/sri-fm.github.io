"""Deterministic UTF-8 BibTeX exports from reviewed publication metadata."""
import hashlib
import re
import unicodedata

TYPES = {'Conference Papers': 'inproceedings', 'Journal Articles': 'article',
         'Technical Reports': 'techreport', 'Book Chapters': 'incollection',
         'Books': 'book', 'Manuals': 'manual', 'Theses': 'phdthesis',
         'Slides': 'misc', 'Preprints and Working Papers': 'unpublished'}

def citation_key(record):
    if record.get('citation_key'):
        return record['citation_key']
    identity = '|'.join((record['title'], record['category'], record['venue_group']))
    surname = record['authors'][0].split(',')[0] if ',' in record['authors'][0] else record['authors'][0].split()[-1]
    surname = unicodedata.normalize('NFKD', surname).encode('ascii', 'ignore').decode()
    surname = re.sub('[^a-zA-Z0-9]', '', surname).lower()
    return f"{surname}{record['year']}-{hashlib.sha256(identity.encode()).hexdigest()[:10]}"

def escape(value):
    replacements = {'\\': r'\textbackslash{}', '{': r'\{', '}': r'\}',
                    '&': r'\&', '%': r'\%', '#': r'\#', '_': r'\_',
                    '$': r'\$', '~': r'\textasciitilde{}', '^': r'\textasciicircum{}'}
    return ''.join(replacements.get(c, c) for c in str(value))

def bibtex(record):
    category = record['category']
    fields = {'author': ' and '.join(('{' + escape(a) + '}') if a in record.get('corporate_authors', []) else escape(a) for a in record['authors']),
              'title': '{' + escape(record['title']) + '}', 'year': str(record['year'])}
    venue_field = {'Conference Papers': 'booktitle', 'Journal Articles': 'journal',
                   'Book Chapters': 'booktitle'}.get(category)
    if venue_field and record['venue']:
        fields[venue_field] = escape(record.get('bibtex_venue', record['venue']))
    if record['report_number']:
        fields['number'] = escape(record['report_number'])
    for name in ('institution', 'publisher', 'volume', 'number', 'pages', 'edition', 'school', 'month', 'isbn', 'series'):
        if record.get(name):
            fields[name] = escape(record[name]).replace('–', '--') if name == 'pages' else escape(record[name])
    doi = record.get('doi')
    if not doi:
        for url in [record['url'], *(link[1] for link in record['links'])]:
            match = re.search(r'(10\.\d{4,9}/[^\s?#]+)', url)
            if match:
                doi = match.group(1)
                break
    if doi:
        fields['doi'] = doi
    fields['url'] = record['url']
    note = record['note']
    if category == 'Slides':
        note = 'Slides. ' + note
    if category == 'Preprints and Working Papers':
        note = 'Unpublished working paper. ' + note
    if note:
        fields['note'] = escape(note.strip())
    return '@' + TYPES[category] + '{' + citation_key(record) + ',\n' + ',\n'.join(
        '  ' + key + ' = {' + value + '}' for key, value in fields.items()) + '\n}\n'
