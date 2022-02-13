# Developer Notes for Contributing Code

Developers who would like to contribute with feature requests, bug reports and other changes are welcome to do so.
Please adhere to the following guidelines when contributing code to this repository.

## Versioning

The library / CLI app is versioned as per the [semantic versioning](https://semver.org/) scheme.
In brief, the version numbers signify the following:

```
<major>.<minor>.<patch>
   |       |       |------ backwards-compatible (no new feature)
   |       |-------------- backwards-compatible (new features or deprecations)
   |---------------------- breaking change
```

## Issues

Issues are used to document and track bugs, feature requests, or anything that should be added, updated, or removed from the codebase.
Questions or concerns can of course be posed via issues.
A contributing developer mainly operns an issue as a means to communicate with the maintainer.

Before opening an issue, please check if the following conditions are met:

1. The issue is related to RenameRename (as opposed to the shell)
2. There exists no similar issue (open or closed)

When opening an issue, please include the following information in the description:

1. RenameRename version number
2. OS and its version number
3. Observed behavior and steps to reproduce it
4. Expected behavior and if applicable, a resolution

## Committing Code to Git

Please follow the [Conventional Changelog](https://www.conventionalcommits.org/en/v1.0.0/) strategy when writing commit messages.

## Code Style

To ensure code style compliance to PEP8, we typically use [flake8](https://www.github.com/PyCQA/flake8).
All Python code contributed should be style compliant.
So, before committing any code, run `flake8` to make these checks.

You can install `flake8` via:

```sh
pip install flake8==3.8.4
```

A configuration file for `flake8` is already provided in `./.flake8`.
Therefore, you can just run the command in the repository's root directory:

```sh
flake8
```

## Unit Tests

RenameRename is tested through unit tests.
If applicable and when contributing Python code, please add a unit test that fails until the bug is resolved or the feature is implemented.
Also, please ensure that already existing tests pass.
