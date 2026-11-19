# Commands for developing, testing, building, and releasing DCMI.

VENV_DIR ?= .venv
VENV_RECREATE ?= false
VENV_RELEASE ?= false

UV_RUN = UV_PROJECT_ENVIRONMENT="$(VENV_DIR)" uv run

.PHONY: setup-venv
setup-venv:
	@command -v uv >/dev/null 2>&1 || { echo "Error: uv is required. Install it from https://docs.astral.sh/uv/."; exit 1; }
	@if [ "$(VENV_RECREATE)" = "true" ] || [ "$(VENV_RECREATE)" = "TRUE" ]; then \
		rm -rf "$(VENV_DIR)"; \
	fi
	@if [ "$(VENV_RELEASE)" = "true" ] || [ "$(VENV_RELEASE)" = "TRUE" ]; then \
		UV_PROJECT_ENVIRONMENT="$(VENV_DIR)" uv sync --extra release; \
	else \
		UV_PROJECT_ENVIRONMENT="$(VENV_DIR)" uv sync --all-extras; \
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
	UV_PROJECT_ENVIRONMENT="$(VENV_DIR)" uv build
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
clean: setup-venv
	$(UV_RUN) python scripts/clean.py $(if $(filter true TRUE 1,$(CLEAN_CONFIRM)),--yes,)
