Python-Core
===

![Python badge](https://badgen.net/pypi/python/black)
![Test badge](https://github.com/python/cpython/actions/workflows/build.yml/badge.svg?branch=main&event=push)

Copyright (C) 2024 @github.com:HungNguyen501.<br>
All rights reserved.<br>

## Short description
The personal project is written mainly by Python. Also, the project uses ***GitHub Action*** and ***Bazel (incremental build model)*** for CI flow that qualifies the following criteria:
- Branch/ Tag naming convention.
- PEP8 coding style.
- Unit Tests - Code coverage 100%.

## Development guides
### Prerequisites
- Bazel
```bash
$ bazel --version
bazel 7.2.1
```
- Python 3.12
```bash
$ python3.12 --version
Python 3.12.7
$ python3.12 -m pip --version
pip 24.2
```
- Githooks: run `make githook` to add the script to pre-commit in githooks.
- Install libs: `make install`
