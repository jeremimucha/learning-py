# Configuration files for testing

Go for the following test directory tree:
project
├── ... top level project files, src dir, docs, etc ...
├── pytest.ini
└── tests
    ├── conftest.py
    ├── api
    │   ├── __init__.py
    │   ├── conftest.py
    │   ├── test_add.py
    │   └── ... test files for api ...
    └── cli
        ├── __init__.py
        ├── conftest.py
        ├── test_add.py
        └── ... test files for cli ...

The `pytest.ini` can also be replaced by a `tox.ini` or `pyproject.toml` or `setup.cfg`
The `__init__.py` files in test subdirectories allow for test files with the same name
to coexist in different test directories.
