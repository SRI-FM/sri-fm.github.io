EMACS ?= emacs
PORT ?= 1313

.PHONY: build clean serve

build:
	$(EMACS) --batch -Q --load ./publish.el --funcall sri-publish

clean:
	$(EMACS) --batch -Q --load ./publish.el --funcall sri-clean

serve: build
	python3 -m http.server $(PORT) --directory public
