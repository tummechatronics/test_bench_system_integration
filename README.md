# System Integration

## Content of the Repository

This repository contains scripts and modules to execute web interface for testing and integration. Furthermore, it handles control of test benches, perform measurement and data processing


* [readme](README.md)
* [changelog](CANGELOG.md)
* [project configuration](pyproject.toml)
* [build script](build_wheel.sh)

The source code directory `system_integration` contains the required structure of the app:
**here come template for frontend + backend**
* [dynamic versioning](system_integration/version.py)
* [package initializer](system_integration/__init__.py)
* [application script](system_integration/app.py)

Unit tests are inside of `tests`
* [test to be executed by PyTest](tests/test_template.py)

Example source code in [system_integration](system_integration) contains:

* [recursive searching for files](system_integration/files.py)
* [application](system_integration/app.py) opening an iPython console

## Description of the Package

Brief description of:

* how to import the module
* how to use the module
* where to find more information

## Contribution guidelines

Before opening a pull-request:

- add entries in the [changelog](CHANGELOG.md).
- increment the [version](system_integration/version.py).
- add and update [tests](tests/).
- make sure that this [readme](README.md) is up-to-date.
- make sure that the [example script](example_template.py) is up-to-date.
- build, lint, test the package.
  ```bash
  ./build_wheel.py
  ```


![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)
![Checked with ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)
![Checked with pyright](https://microsoft.github.io/pyright/img/pyright_badge.svg)
