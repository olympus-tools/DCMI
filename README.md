# DCMI

DCMI is a Python interface for reading and writing `*.dcm` parameter files.

## Requirements

- Linux or Windows
- Python 3.13.7 through Python 3.14
- [uv](https://docs.astral.sh/uv/)

## Development setup

Use the newest supported Python installed on the system:

```shell
make setup-venv
```

The single environment is `.venv`. Dependencies are resolved from `uv.lock`;
do not install project dependencies with pip. CI uses separate jobs to verify
the minimum and newest supported Python versions.

## Checks and builds

```shell
make format-check
make lint
make type-check
make test-requirements
make test-coverage
make build-package
```

`make clean` removes generated files after confirmation. CI uses
`make clean CLEAN_CONFIRM=true`.

## Releases

DCMI uses `setuptools-scm`. See [the release checklist](docs/prj/release_checklist.md)
for the manual tag and changelog process.
