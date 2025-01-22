.PHONY: init
init:
	@pipenv install --dev

.PHONY: ci
ci:
	pipenv check
	pipenv run ci

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
	python -m json2dot.cli -o $@ < $<
