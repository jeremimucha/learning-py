# Building pytest plugins

Example of how to build and publish a pytest plugin

## `slow` tests plugin

By default pytest runs all tests. If some of those tests are slow to execute,
and marked with `@pytest.mark.slow`, it's possible to exclude the slow tests
but it has to be done explicitly every time - `pytest -m "not slow"`.
Well override this behavior with a plugin that achieves the following:

|Behavior    |Without plugin      |With plugin          |
|------------|--------------------|---------------------|
|Exclude slow|pytest -m "not slow"|pytest               |
|Include slow|pytest              |pytest --slow        |
|Only slow   |pytest -m slow      |pytest -m slow --slow|


Pytest behavior can be modified via hook functions:

* https://docs.pytest.org/en/6.2.x/writing_plugins.html#writinghooks
* https://docs.pytest.org/en/latest/reference/reference.html#hook-reference

In this case notable hooks are:
* `pytest_configure()` - hook for plugins and conftest files to perform initial configuration.
* `pytest_addoption()` - Used to register options and settings.
* `pytest_collection_modifyitems()` - Called after test collection has been performed and can
  be used to filter or re-order the test items.
