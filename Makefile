.PHONY: init
init:
	@uv sync

.PHONY: clean
clean:
	@rm -rf build dist .pytest_cache .tox
	@find . -name "*.egg" -exec rm -rf {} +
	@find . -name "*.egg-info" -exec rm -rf {} +
	@find . -name "*.pyc" -delete
	@find . -name "__pycache__" -exec rm -rf {} +
	@find . -name ".mypy_cache" -exec rm -rf {} +

TEST_SOURCE := tests/test.json
TEST_IMAGE := tmp/debug.svg

.PHONY: $(TEST_IMAGE)
$(TEST_IMAGE): $(TEST_SOURCE)
	@mkdir -p tmp
	uv run python -m json2dot.cli -o $@ < $<

.PHONY: check
check:
	uvx tox -e black,ruff,mypy -p 3

.PHONY: test
test:
	uvx tox -e py312

.PHONY: ci
ci:
	uvx tox -e black,ruff,mypy,py312 -p 4

.PHONY: dev
dev:
	pip install --editable .

.PHONY: install
install:
	pip install .

.PHONY: dist
dist:
	uv run python setup.py sdist
