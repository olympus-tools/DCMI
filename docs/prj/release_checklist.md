# DCMI release checklist

1. Update `CHANGELOG.md` and move the relevant entries from `Unreleased` to
   `## [<version>]`.
2. Verify that the version is a valid SemVer value and that the planned tag is
   `v<version>`.
3. Run:

   ```shell
   make format-check
   make lint
   make type-check
   make test-requirements
   make build-package
   ```

4. Run `make release-checklist` on the tagged commit. It verifies the tag, the
   changelog section, and a clean working tree.
5. Upload artifacts manually after the checklist succeeds.

The migration prepares `v0.1.0`; creating tags and uploading packages are
maintainer actions and are not automated by the Makefile.
