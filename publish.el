;;; publish.el --- Build the SRI Formal Methods website  -*- lexical-binding: t; -*-

(require 'ox-html)
(require 'ox-publish)
(require 'subr-x)

(org-link-set-parameters
 "site"
 :export
 (lambda (path description backend _info)
   (if (org-export-derived-backend-p backend 'html)
       (format "<a href=\"/%s\">%s</a>"
               (string-remove-prefix "/" path)
               (or description (sri--html-text path)))
     (or description path))))

(org-link-set-parameters
 "siteimg"
 :export
 (lambda (path description backend _info)
   (if (org-export-derived-backend-p backend 'html)
       (format "<img src=\"/%s\" alt=\"%s\" class=\"lead-image\">"
               (string-remove-prefix "/" path)
               (sri--html-text (or description "")))
     (or description path))))

(defconst sri-root-directory
  (file-name-directory (or load-file-name buffer-file-name)))

(defconst sri-content-directory
  (expand-file-name "content" sri-root-directory))

(defconst sri-public-directory
  (expand-file-name "public" sri-root-directory))

(defun sri--html-text (text)
  "Encode TEXT for safe use in HTML."
  (org-html-encode-plain-text (or text "")))

(defun sri-html-special-block (special-block contents info)
  "Export site-specific SPECIAL-BLOCK elements to HTML.

The Org source supports two deliberately small extensions:

  #+begin_details Title
  ...
  #+end_details

  #+begin_talk Speaker | Title
  ...
  #+end_talk"
  (let* ((type (downcase (or (org-element-property :type special-block) "")))
         (label (string-trim
                 (or (org-element-property :parameters special-block) ""))))
    (cond
     ((string= type "details")
      (format
       (concat "<details class=\"entry\">\n"
               "<summary>%s</summary>\n"
               "<div class=\"entry-body\">\n%s</div>\n"
               "</details>")
       (sri--html-text label)
       contents))
     ((string= type "talk")
      (let* ((parts (split-string label "[ \t]*|[ \t]*"))
             (speaker (string-trim (or (car parts) "")))
             (title (string-trim (mapconcat #'identity (cdr parts) " | "))))
        (format
         (concat "<details class=\"talk\">\n"
                 "<summary><strong>%s</strong><span>%s</span></summary>\n"
                 "<div class=\"talk-body\">\n%s</div>\n"
                 "</details>")
         (sri--html-text speaker)
         (sri--html-text title)
         contents)))
     (t (org-html-special-block special-block contents info)))))

(load (expand-file-name "scripts/source-highlight.el"
                        (file-name-directory (or load-file-name buffer-file-name))))

(org-export-define-derived-backend 'sri-html 'html
  :translate-alist '((special-block . sri-html-special-block)
                     (src-block . sri-html-source-block)))

(defun sri-publish-to-html (property-list filename publishing-directory)
  "Publish FILENAME with the `sri-html' backend."
  (org-publish-org-to
   'sri-html filename ".html" property-list publishing-directory))

(defun sri--current-section (info)
  "Return the top-level site section for export INFO."
  (let* ((input (plist-get info :input-file))
         (relative (and input
                        (file-relative-name input sri-content-directory))))
    (cond
     ((or (null relative) (string= relative "index.org")) "home")
     (t (file-name-sans-extension
         (car (split-string relative "/")))))))

(defun sri--nav-link (label href section current)
  "Return one navigation link."
  (format "<a href=\"%s\"%s>%s</a>"
          href
          (if (string= section current) " aria-current=\"page\"" "")
          label))

(defun sri-html-preamble (info)
  "Return the shared site header for export INFO."
  (let ((current (sri--current-section info)))
    (concat
     "<a class=\"skip-link\" href=\"#content\">Skip to content</a>\n"
     "<header class=\"site-header\">\n"
     "  <div class=\"site-header__inner\">\n"
     "    <a class=\"site-mark\" href=\"/\" aria-label=\"SRI Formal Methods Program home\">\n"
     "      <img src=\"/images/SRI_Lockup_Horizontal_Black_RGB.png\" alt=\"SRI International\">\n"
     "      <span>Formal Methods Program</span>\n"
     "    </a>\n"
     "    <nav class=\"site-nav\" aria-label=\"Primary\">\n"
     "      " (sri--nav-link "Home" "/" "home" current) "\n"
     "      " (sri--nav-link "About" "/about/" "about" current) "\n"
     "      " (sri--nav-link "Tools" "/tools/" "tools" current) "\n"
     "      " (sri--nav-link "Media" "/media/" "media" current) "\n"
     "      " (sri--nav-link "Publications" "/pubs/" "pubs" current) "\n"
     "      " (sri--nav-link "Events" "/events/" "events" current) "\n"
     "      " (sri--nav-link "Blog" "/blog/" "blog" current) "\n"
     "      " (sri--nav-link "Impact" "/impact/" "impact" current) "\n"
     "    </nav>\n"
     "  </div>\n"
     "</header>")))

(defun sri-html-postamble (_info)
  "Return the shared site footer."
  (concat
   "<footer class=\"site-footer\">\n"
   "  <div class=\"site-footer__inner\">\n"
   "    <span>SRI Formal Methods Program</span>\n"
   "    <a href=\"https://www.sri.com/\">SRI International</a>\n"
   "  </div>\n"
   "</footer>"))

(setq org-export-with-section-numbers nil
      org-export-with-smart-quotes nil
      org-export-with-toc nil
      org-export-with-latex nil
      org-export-time-stamp-file nil
      org-html-doctype "html5"
      org-html-html5-fancy t
      org-html-head-include-default-style nil
      org-html-head-include-scripts nil
      org-html-with-latex nil
      org-html-validation-link nil
      org-publish-timestamp-directory
      (expand-file-name ".cache/org-publish/" sri-root-directory)
      org-publish-use-timestamps-flag nil)

(setq org-publish-project-alist
      `(("site-pages"
         :base-directory ,sri-content-directory
         :base-extension "org"
         :publishing-directory ,sri-public-directory
         :recursive t
         :publishing-function sri-publish-to-html
         :headline-levels 5
         :section-numbers nil
         :with-author nil
         :with-creator nil
         :with-date nil
         :with-latex nil
         :with-toc nil
         :html-doctype "html5"
         :html-html5-fancy t
         :html-head
         "<link rel=\"stylesheet\" href=\"/css/site.css\">\n<meta name=\"theme-color\" content=\"#17364f\">"
         :html-preamble sri-html-preamble
         :html-postamble sri-html-postamble)
        ("site-static"
         :base-directory ,(expand-file-name "static" sri-root-directory)
         :base-extension
         "css\\|js\\|txt\\|jpg\\|jpeg\\|png\\|gif\\|webp\\|svg\\|eps\\|ico\\|pdf\\|bib"
         :publishing-directory ,sri-public-directory
         :recursive t
         :publishing-function org-publish-attachment)
        ("site"
         :components ("site-pages" "site-static"))))

(defun sri-arrange-html-output ()
  "Arrange flat Org sources into clean directory-style public routes."
  (dolist (source
           (directory-files-recursively sri-content-directory "\\.org\\'"))
    (let* ((relative (file-relative-name source sri-content-directory))
           (route (file-name-sans-extension relative)))
      (unless (member route '("index" "404"))
        (let ((generated
               (expand-file-name (concat route ".html")
                                 sri-public-directory))
              (target
               (expand-file-name (concat route "/index.html")
                                 sri-public-directory)))
          (unless (file-exists-p generated)
            (error "Expected generated page is missing: %s" generated))
          (make-directory (file-name-directory target) t)
          (rename-file generated target t))))))

(defun sri-clean ()
  "Remove generated output and the local Org publishing cache."
  (interactive)
  (unless (string= (file-name-nondirectory
                    (directory-file-name sri-public-directory))
                   "public")
    (error "Refusing to clean unexpected output path: %s"
           sri-public-directory))
  (when (file-directory-p sri-public-directory)
    (delete-directory sri-public-directory t))
  (when (file-directory-p org-publish-timestamp-directory)
    (delete-directory org-publish-timestamp-directory t))
  (let ((cache-root (expand-file-name ".cache" sri-root-directory)))
    (when (and (file-directory-p cache-root)
               (null (directory-files
                      cache-root nil directory-files-no-dot-files-regexp)))
      (delete-directory cache-root))))

(defun sri-publish ()
  "Build the complete website."
  (interactive)
  (sri-clean)
  (make-directory sri-public-directory t)
  (org-publish "site" t)
  (sri-arrange-html-output))

(provide 'publish)
;;; publish.el ends here
