# SRI Formal Methods Program website

The site is edited in Org mode and exported to static HTML with Emacs. There is
no package manager, theme, or site-generator dependency.

## Edit

The main pages are flat Org files in `content/`: `index.org`, `about.org`,
`tools.org`, `media.org`, `pubs.org`, `events.org`, `blog.org`, and
`impact.org`. Blog posts are separate files in `content/blog/`. Add a post
there, then link it from `content/blog.org`.

Images live in `static/images/`, and shared styles live in
`static/css/site.css`.

The publications page is generated from `data/publications.json`. Edit that
file, retain the evidence URLs in each record's `sources`, then run
`python3 scripts/render_publications.py`. Run the same command with `--check`
to validate the records and confirm that the Org page is current. Publications
are grouped only by year, newest first, and sorted by title within each year.
Publication type, venue, report number, and version notes remain entry metadata.
The page documents archive coverage and known gaps; the collection is not an
exhaustive institutional bibliography.

The exporter also understands two small Org blocks:

```org
#+begin_details Section title
Content
#+end_details

#+begin_talk Speaker name | Talk title
Content
#+end_talk
```

## Build

Install Emacs 29 or newer and Python 3 on macOS or Linux, then run:

```sh
make build
```

The generated site is written to `public/` and is intentionally not committed.
To preview it locally:

```sh
make serve
```

Open <http://localhost:1313>. Pushing `main` rebuilds and deploys the site with
GitHub Pages.

The local server watches `content/`, `static/`, `examples/tools/`,
`publish.el`, and the static source highlighter. After a
successful rebuild, open preview tabs refresh automatically. The reload client
is injected by the local server only; it is never written to `public/` or
deployed. Use `make serve PORT=1314` to choose another local port. Build errors
appear in the terminal; saving a correction triggers another build.

Use `make build` and `make clean` for publishing operations. Both share a local
process lock, so a manual build and the preview watcher cannot modify the Org
cache or generated output concurrently. Waiting builds resume automatically.

The Tools showcase includes its code directly from `examples/tools/`. Validation
commands, results, source references, and highlighting provenance are recorded in
`examples/tools/validation.org`. Deferred tool descriptions remain in a COMMENT
subtree of `content/tools.org` and do not export.

## Publications and citations

`data/publications.json` is the canonical bibliography. Each record retains its
source URLs and a persistent `citation_key`. Edit metadata there, then run:

```sh
python3 scripts/render_publications.py
make build
python3 scripts/render_publications.py --check
python3 scripts/check_publications.py
```

The renderer produces the year-only bibliography, a native collapsed BibTeX
control for every record, one `static/bib/<citation_key>.bib` download per record,
and `static/bib/publications.bib`. The generated directory is owned by the
renderer; obsolete generated citations are removed. No client-side JavaScript
is needed. The local watcher reloads changes to the generated Org and BibTeX.

Keep an assigned citation key unchanged when correcting metadata. New keys are
deterministically derived from the first author, year, and a title/category/venue
identity hash; duplicate keys are rejected. Publication types map to standard
BibTeX entry types. Corporate author names are brace-protected, personal names
are separated with `and`, title capitalization is protected, and TeX special
characters in text fields are escaped. Names and titles retain Unicode in UTF-8;
use a Unicode-capable bibliography/LaTeX workflow (for example BibLaTeX/Biber)
when typesetting accented names. Unknown fields are omitted rather than guessed.

The validation script uses the real TeX Live `bibtex` parser and name formatter,
then checks the built HTML for unique anchors, initially collapsed citations,
exact citation text, and byte-identical downloadable files. It requires BibTeX
on PATH (with a fallback to the installed macOS TeX Live 2025 binary).

`data/cav-audit-2026-10-09.json` records the four-author CAV reconciliation,
including the 23-paper expected set, eight additions, and affiliation exceptions.
`data/neumann-cheri-audit-2026-10-09.json` records the source inventories,
selection decisions, version distinctions, counts, and unresolved metadata.
`data/cheri-sri-affiliation-audit-2026-10-09.json` supersedes the initial broad
project import: it reviews 104 entries, retains 62 with direct SRI authorship,
and records 42 removals with publication-time affiliation evidence. The final
bibliography has 384 records. Collaboration or sponsorship alone does not
qualify; historical SRI employment is not carried forward to later papers.
The Morello performance report lacks a complete affiliation table and is
excluded because direct SRI authorship was not established. These audits
describe coverage of the named sources, not universal completeness.

## CHERI figure attribution

`static/images/cheri-protection-model.png` is a genuine, unchanged diagram
cropped from Figure 2.1, page 46 of *Capability Hardware Enhanced RISC
Instructions: CHERI Instruction-Set Architecture (Version 9)*, UCAM-CL-TR-987,
September 2023, by Robert N. M. Watson et al. Copyright the listed report authors
and SRI International. The report's page 2 explicitly licenses it under
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), excluding the
University marks (none are included in this crop).

[Official source PDF](https://www.cl.cam.ac.uk/techreports/UCAM-CL-TR-987.pdf#page=46).
Rendered with Poppler at 300 dpi; crop fractions of the rendered page are
(left=.116, top=.116, right=.885, bottom=.269), yielding 1908 × 537 pixels.
Only surrounding page text and whitespace were removed. No AI redrawing,
retouching, label changes, or recoloring. The page caption provides attribution,
license, source, and a full-resolution link.

### Impact timeline

`data/impact-history.json` maintains the 47 historical contribution items,
selected SRI contributors, collaborator distinctions, attribution gaps, and
source provenance. Removed timeline entries remain in non-rendered audit data.
Edit that file, then run `python3 scripts/render_impact.py` to regenerate
`content/impact.org`; `python3 scripts/render_impact.py --check` validates coverage
and detects stale output. Keep unresolved affiliations in the non-rendered `gap`
and `note` provenance fields; use `public_note` for verified historical context.
The renderer omits contributor rows without supported names. Verify
publication-time affiliation before adding a contributor. The timeline's native
`details` work without scripting; `static/js/impact-history.js` adds desktop
hover/focus, exclusive panels, Escape dismissal, and viewport positioning.
