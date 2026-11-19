# Commands for developing, testing, building, and releasing DCMI.

UV_RUN = uv run
UPGRADE ?= true
LOCKED ?= false
REINSTALL_PACKAGE ?=

.PHONY: setup-venv
setup-venv:
	@command -v uv >/dev/null 2>&1 || { echo "Error: uv is required. Install it from https://docs.astral.sh/uv/."; exit 1; }
	echo "Syncing project dependencies:"
	@if [ "$(LOCKED)" = "true" ] || [ "$(LOCKED)" = "TRUE" ] || [ "$(LOCKED)" = "1" ]; then \
		uv sync --all-extras --locked $(if $(REINSTALL_PACKAGE),--reinstall-package $(REINSTALL_PACKAGE),); \
	elif [ "$(UPGRADE)" = "true" ] || [ "$(UPGRADE)" = "TRUE" ] || [ "$(UPGRADE)" = "1" ]; then \
		uv sync --all-extras --upgrade $(if $(REINSTALL_PACKAGE),--reinstall-package $(REINSTALL_PACKAGE),); \
	else \
		uv sync --all-extras $(if $(REINSTALL_PACKAGE),--reinstall-package $(REINSTALL_PACKAGE),); \
	fi

.PHONY: test-requirements
test-requirements: setup-venv
	$(UV_RUN) pytest

.PHONY: test-coverage
test-coverage: setup-venv
	$(UV_RUN) pytest --cov=dcmi --cov-report=html --cov-report=term-missing

.PHONY: format
format: setup-venv
	$(UV_RUN) ruff format .

.PHONY: format-check
format-check: setup-venv
	$(UV_RUN) ruff format --check .

.PHONY: lint
lint: setup-venv
	$(UV_RUN) ruff check .

.PHONY: type-check
type-check: setup-venv
	$(UV_RUN) pyright

.PHONY: build-package
build-package: setup-venv
	rm -rf dist
	uv build
	$(UV_RUN) twine check dist/*.whl dist/*.tar.gz

.PHONY: release-checklist
release-checklist: setup-venv
	$(UV_RUN) python scripts/release_check.py

.PHONY: release-changelog
release-changelog: setup-venv
	$(UV_RUN) python scripts/release_check.py --changelog-only

.PHONY: thirdpartycheck
thirdpartycheck: setup-venv
	$(UV_RUN) python scripts/analyze_dependencies.py --format json --generate-notice --check-compatibility

.PHONY: release
release: release-checklist release-changelog thirdpartycheck build-package
	@echo "Release checks and artifacts completed. Tagging and uploading remain manual."

.PHONY: clean
clean:
	$(UV_RUN) python scripts/clean.py $(if $(filter true TRUE 1,$(CLEAN_CONFIRM)),--yes,)
