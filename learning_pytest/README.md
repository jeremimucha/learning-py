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
