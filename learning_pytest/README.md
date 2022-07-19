# Learning pytest

## Prepare the environment:

1. Setup a virtualenv
   `python -m venv .venv`
   `. .venv/bin/activate`
2. Install the application under test and the dependencies
   `pip install pytest`
   `pip install ./cards_proj`
3. Write and run tests
   `pytest <test-file-or-dir>`


## Executing tests

pytest allows for running a subset of tests in several ways:

|Subset|Syntax|
|------|-------|
|Single test method              |  pytest path/test_module.py::TestClass::test_method |
|All tests in a class            |  pytest path/test_module.py::TestClass              |
|Single test function            |  pytest path/test_module.py::test_function          |
|All tests in a module           |  pytest path/test_module.py                         |
|All tests in a directory        |  pytest path                                        |
|Tests matching a name pattern   |  pytest -k pattern                                  |


## Useful flags

* `-s/--capture=no`  - doesn't capture stdout/stderr
* `-v/-vv`  - different levels of verbosity
* `-r` - report reasons for different test results (e.g. skipping a test)
  The charater(s) that follow the `-r` flag specify which events should
  be reported:
  - `f` - failed
  - `E` - Errors
  - `a` - all, except for passed
* `--setup-show` - shows setup of fixtures

## Running markers

Run tests based on markers:

- run only tests marked `exception`
  `pytest -v -m exception`
- run only  tests marked `smoke`
  `pytest -v -m smoke`
