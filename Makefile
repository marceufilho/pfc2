UV ?= uv
PNPM ?= pnpm

.PHONY: help sync test check eval freeze-check site-data site-install site-build site-dev site-test

help:
	@echo "sync          create the locked Python environment"
	@echo "test          tests only"
	@echo "check         tests, lint, format check and types"
	@echo "eval          run the evaluation harness: make eval EVAL_ARGS='selfcheck --output NEW --dry-run'"
	@echo "freeze-check  compare the tree with the frozen candidate (validation/freeze)"
	@echo "site-data     regenerate the site's checker bundle, program data and docs pages (SITE_ARGS=--check compares)"
	@echo "site-build    build the static site into site/dist (needs Node 24 and pnpm)"
	@echo "site-dev      development server"
	@echo "site-test     browser tests in Chromium (pnpm --dir site exec playwright install chromium, once)"
	@echo "Run the tool itself with: uv run pfc2 --help"

sync:
	$(UV) sync --locked

test:
	$(UV) run --locked pytest

check:
	$(UV) run --locked pytest
	$(UV) run --locked ruff check .
	$(UV) run --locked black --check --line-length 120 .
	$(UV) run --locked mypy
	$(UV) run --locked mypy --strict pfc2_eval
	$(UV) run --locked python tools/site_data.py --check

eval:
	$(UV) run --locked python -m pfc2_eval $(EVAL_ARGS)

freeze-check:
	$(UV) run --locked python tools/freeze.py --check

site-data:
	$(UV) run --locked python tools/site_data.py $(SITE_ARGS)

site-install:
	$(PNPM) --dir site install --frozen-lockfile
	node site/scripts/prepare-engine.mjs

site-build: site-install
	$(PNPM) --dir site build

site-dev: site-install
	$(PNPM) --dir site dev

site-test: site-build
	$(PNPM) --dir site exec playwright test
