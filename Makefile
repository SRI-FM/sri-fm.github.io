EMACS ?= emacs
PORT ?= 1313

.PHONY: build clean serve

build:
	python3 scripts/build_lock.py $(EMACS) --batch -Q --load ./publish.el --funcall sri-publish

clean:
	python3 scripts/build_lock.py $(EMACS) --batch -Q --load ./publish.el --funcall sri-clean

serve: build
	python3 scripts/dev_server.py --port $(PORT)
