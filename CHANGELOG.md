# Changelog

All notable changes to this project will be documented in this file.
The format is based on [Keep a Changelog], and the project adheres to
[Semantic Versioning].

[Keep a Changelog]:
https://keepachangelog.com/en/1.0.0/
[Semantic Versioning]:
https://semver.org/spec/v2.0.0.html


## [Unreleased]

### Added
- GitHub workflow.
- Authors and changelog files.
- Copyright headers in all source code files.

### Changed
- Move test files outside of the package source code folder.

### Fixed
- Set library requirements and doc/lint/test requirements.
- Make source code comply with latest Flake8 and PyLint rules.
- Fix invalid `str.format` syntax for Python 2.6.

## [1.0.0] - 2019-02-03

### Added
- Initial Python implementation of the SSolar-GOA model:
  - Core classes `Atmosphere` and `Geometry`.
  - Main radiative transfer function `radtran`.
  - First library tests.


[Unreleased]:
https://github.com/molinav/solo/compare/v1.0.0...develop
[1.0.0]:
https://github.com/molinav/solo/tree/v1.0.0

[CVE-2021-33430]:
https://nvd.nist.gov/vuln/detail/CVE-2021-33430
