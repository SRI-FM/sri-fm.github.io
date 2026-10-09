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

Install Emacs 29 or newer, then run:

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
