# Contributing to DCMI

## Setup

Install uv and a supported system Python:

```shell
make setup-venv
```

The local environment is always `.venv` and follows the newest supported
system Python selected by uv. CI tests the minimum and newest supported
versions independently.

## Development workflow

Run the same checks as CI through Make:

```shell
make format
make lint
make type-check
make test-requirements
make test-coverage
make build-package
```

Keep `pyproject.toml` direct dependency pins and `uv.lock` synchronized. Use
stable PyPI releases only, and choose versions compatible with both supported
Python versions.

## Documentation and pull requests

Update the relevant Markdown documentation when commands or supported versions
change. Pull requests need one of the `documentation`, `feature`, `bugfix`, or
`test` labels.
