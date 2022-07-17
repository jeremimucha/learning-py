# Builtin fixtures

* tmp_path - function scope fixture; gives access to a temporary path
* tmp_path_factory - session scope fixture; provides a factory of temporary paths
* capsys - captures stdout and stderr
* capfd - captures file destrictors 1 and 2
* capsysbinary - captures stdout and stderr but as bytes
* capfdbinary - fd 1 and 2 as bytes
* caplog - captures output written with the `logging` package


## Monkeypatching

The `monkeypatch` fixture provides basic mocking facilities,
that allows us to change object behavior at runtime.

`monkeypatch` interface:
* setattr(target, name, value, raising=True) - sets an attribute
* delattr(target, name, raising=True) - deletes an attribute
* setitem(dic, name, value) - sets a dictionary entry
* delitem(dic, name, raising=True) - deletes a dictionary entry
* setenv(name, value, prepend=None) - sets an environment variable
* delenv(name, raising=True) - deletes an environment variable
* syspath_prepend(path) - prepends path to sys.path
* chdir(path) - changes the current working directory

`raising=True` raises and exception if the given item doesn't already exist.

Use of `monkeypatch` generally requires knowledge of the implementation
of the application under test.
