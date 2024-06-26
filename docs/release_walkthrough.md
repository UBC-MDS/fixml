# Release walkthrough

This is a walkthrough of the fixml 0.1.0 release for building with Poetry 
and uploading the wheels to PyPI.

The commands can be copied into the command line, but be sure to replace any 
version shown in this file to the correct version.

## Preparation

Before starting the release workflow, tokens for uploading the package to 
PyPI/TestPyPI need to be set up. This setup is an on-time setup per host or 
per environment.

### TestPyPI

1. Add repository to Poetry config

```bash
poetry config repositories.test-pypi https://test.pypi.org/legacy/
```

2. Get token from https://test.pypi.org/manage/account/token/

3. Store token using in Poetry:
```bash
poetry config pypi-token.test-pypi $TESTPYPI_TOKEN
```

### PyPI

1. Get token from https://pypi.org/manage/account/token/

2. Store token using in Poetry:
```bash
poetry config pypi-token.pypi $PYPI_TOKEN
```

## Release workflow

Each time before releasing a new version, a version bumping action needs to 
be taken. This can be managed and done by using Poetry. The version naming 
follows [SemVer 2.0.0, or semantic versioning 2.0.0](https://semver.org/).

### Bump version

You can choose to bump to different versions:

Bump up one prerelease version: 
```bash
poetry version prerelease
```

Bump up one patch version:
```bash
poetry version patch
```

Bump up one minor version:
```bash
poetry version minor
```

Bump up one major version:
```bash
poetry version major
```

When in doubt, one can always add `--dry-run` to the command, to see what 
the version would look like without actually modifying `pyproject.toml`.

### Write changelog

The changeloag is located at `CHANGELOG.md` in the project root. For every 
official releases (non-prerelease), you should always write down what were 
being changed in the new version.

### Create a release tag

You should create a GitHub release or a tag in git, to mark the commit to be 
released with the tag named after the version you want to release. This will 
help ReadtheDocs to render pages specific for the version.

### Publish the Package

#### TestPyPI

```bash
poetry build && poetry publish -r test-pypi
```

#### PyPI
```bash
poetry build && poetry publish
```

If the same version already exist on PyPI/TestPyPI, poetry will return error 
and no new wheel/package files would be uploaded.