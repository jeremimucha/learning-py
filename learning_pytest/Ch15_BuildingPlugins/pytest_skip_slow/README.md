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


## pytest plugin definition

1. Begin with initializing the project using `flit init` (`python -m pip instal flit` first if needed)
2. Fill in the generated `pyproject.toml`
* name is changed to "pytest-skip-slow". Flit assumes the module name and
  package name will be the same. That’s not true of pytest plugins. pytest
  plugins usually start with pytest- and Python doesn’t like module names
  with dashes.
* The actual name of the module is set in the `[tool.flit.module]` section with
  `name = "pytest_skip_slow"`. This module name will also show up in the entry-
  points section.
* The section `[project.entry-points.pytest11]` is added, with one entry `pytest_skip_slow = "pytest_skip_slow.py"`.
  This section name is always the same for pytest plug-ins. It’s defined by pytest.
  The section needs one entry, `name_of_plugin = "plugin_module"`.
  In our case, this is `skip_slow = "pytest_skip_slow"`.
  https://docs.pytest.org/en/latest/how-to/writing_plugins.html#making-your-plugin-installable-by-others
* The classifiers section has been extended to include `"Framework :: Pytest"`, a
  special classifier specifically for pytest plugins.
* dependencies lists dependencies. Because pytest plugins require pytest, we list pytest.
* requires-python is optional. However, I only intend to test against Python versions 3.7 and above.
* section `[project.optional-dependencies]`, `test = ["tox"]` is optional.