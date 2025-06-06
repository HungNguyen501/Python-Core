Python-Core
===

![Python badge](https://badgen.net/pypi/python/black)
![Test badge](https://github.com/python/cpython/actions/workflows/build.yml/badge.svg?branch=main&event=push)

Copyright (C) 2024 @github.com:HungNguyen501.<br>
All rights reserved.<br>

## Short description
The personal project is written mainly by Python. Also, the project uses ***GitHub Action*** and ***Bazel (incremental build model)*** for CI flow that qualifies the following criteria:
- PEP8 coding style.
- Unit Tests - Code coverage `100%`.

## Development guides
### Prerequisites
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
- Bazel
```bash
$ bazel --version
bazel 7.2.1
```
- Python 3.12
```bash
$ python3.12 --version
Python 3.12.7
```
- Init project:
```bash
# Create python venv
$ python3.12 -m venv .venv
$ source .venv/bin/activate
# Install dependencies and githook
$ make init
```
