;;; source-highlight.el --- Static language examples -*- lexical-binding: t; -*-

;; Focused font-lock adaptation of the token categories inspected in:
;; PVS/emacs/pvs-mode.el (pvs-font-lock-keywords-1)
;; sal-3.3/etc/sal-mode.el (sal-font-lock-keywords).
;; Identifiers and numerals remain plain in PVS/SAL, as in those modes.
;; Colors are site CSS, not an attempt to reproduce a user's Emacs theme.
(require 'font-lock)
(require 'ox-html)

(defconst sri-pvs-words
  '("and" "andthen" "array" "as" "assuming" "assumption" "auto_rewrite"
    "auto_rewrite+" "auto_rewrite-" "axiom" "begin" "but" "by" "cases"
    "challenge" "claim" "closure" "codatatype" "coinductive" "cond"
    "conjecture" "containing" "conversion" "conversion+" "conversion-"
    "corollary" "datatype" "else" "elsif" "end" "endassuming" "endcases"
    "endcond" "endif" "endtable" "exists" "exporting" "fact" "false"
    "forall" "formula" "from" "function" "has_type" "if" "iff" "implies"
    "importing" "in" "inductive" "judgement" "lambda" "law" "lemma" "let"
    "library" "macro" "measure" "nonempty_type" "not" "o" "obligation" "of"
    "or" "orelse" "postulate" "proposition" "recursive" "sublemma" "subtypes"
    "subtype_of" "table" "then" "theorem" "theory" "true" "type" "type+"
    "var" "when" "where" "with" "xor"))

(defconst sri-sal-words
  '("context" "type" "begin" "end" "datatype" "module" "array" "of" "with"
    "to" "lambda" "forall" "exists" "let" "in" "if" "then" "else" "elsif"
    "endif" "input" "output" "global" "local" "definition" "initialization"
    "transition" "rename" "theorem" "lemma" "claim" "importing" "prefix"
    "suffix" "ringset" "scalarset" "implements" "observe"))

(defun sri-source-font-lock (language)
  "Set up only the syntax and font-lock needed for LANGUAGE examples."
  (let ((table (make-syntax-table)))
    (modify-syntax-entry ?_ "w" table)
    (modify-syntax-entry ?- "_" table)
    (modify-syntax-entry ?' "_" table)
    (modify-syntax-entry (if (equal language "yices") ?\; ?%) "<" table)
    (modify-syntax-entry ?\n ">" table)
    (set-syntax-table table))
  (setq-local font-lock-defaults
    (list
     (cond
      ((equal language "pvs")
       `((,(regexp-opt sri-pvs-words 'symbols) . font-lock-keyword-face)
         ("[][{}()|]" . font-lock-keyword-face)
         ("[-+*/=<>]+" . font-lock-function-name-face)))
      ((equal language "sal")
       `((,(regexp-opt (append sri-sal-words (mapcar #'upcase sri-sal-words)) 'symbols)
          . font-lock-keyword-face)
         (,(regexp-opt '("and" "not" "or" "xor" "false" "true" "mod" "div"
                        "AND" "NOT" "OR" "XOR" "FALSE" "TRUE" "MOD" "DIV"
                        "ring_succ" "ring_pred" "integer" "natural" "nzinteger"
                        "real" "nzreal" "boolean" "int" "nat" "bool"
                        "INTEGER" "NATURAL" "NZINTEGER" "REAL" "NZREAL" "BOOLEAN") 'symbols)
          . font-lock-variable-name-face)))
      (t
       '(("\\_<\\(define\\|assert\\|check\\|show-model\\)\\_>" . font-lock-keyword-face)
         ("\\_<\\(bitvector\\|int\\|real\\|bool\\)\\_>" . font-lock-type-face)
         ("\\_<bv-add\\_>\\|=" . font-lock-function-name-face)
         ("\\_<0b[01]+\\_>" . font-lock-constant-face))))
     nil (equal language "pvs")))
  (font-lock-ensure))

(defun sri-html-source-block (block contents info)
  "Export supported examples as escaped, static highlighted HTML."
  (let ((language (org-element-property :language block)))
    (if (not (member language '("pvs" "sal" "yices")))
        (org-html-src-block block contents info)
      (let ((source (org-element-property :value block)) pieces)
        (with-temp-buffer
          (insert source)
          (sri-source-font-lock language)
          (let ((pos (point-min)))
            (while (< pos (point-max))
              (let* ((face (get-text-property pos 'face))
                     (next (next-single-property-change pos 'face nil (point-max)))
                     (class (cdr (assq face '((font-lock-keyword-face . "syntax-keyword")
                                             (font-lock-function-name-face . "syntax-operator")
                                             (font-lock-variable-name-face . "syntax-type")
                                             (font-lock-type-face . "syntax-type")
                                             (font-lock-constant-face . "syntax-constant")
                                             (font-lock-comment-face . "syntax-comment")
                                             (font-lock-string-face . "syntax-string")))))
                     (text (org-html-encode-plain-text (buffer-substring-no-properties pos next))))
                (push (if class (format "<span class=\"%s\">%s</span>" class text) text) pieces)
                (setq pos next)))))
        (format "<div class=\"code-example\"><p class=\"code-label\">%s</p><pre tabindex=\"0\" aria-label=\"%s example\"><code>%s</code></pre></div>"
                (if (equal language "yices") "Yices · native input language" (upcase language))
                (upcase language) (apply #'concat (nreverse pieces)))))))
