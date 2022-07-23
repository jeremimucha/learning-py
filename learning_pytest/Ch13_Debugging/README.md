# Debugging test failures


## Debugging environment

It's necessary to setup a new virtualenv specifically for the code we're testing
if we intend to debug and edit the code.
It's super handy to be able to modify the source code an immediately run the tests,
without having to rebuild the package and reinstall it in our virtual environment.

To acomplish this -> install in editable mode.
`pip install -e ./package_dir_name`
To install optional dependencies - i.e. pytest, tox, etc. specify the name of the
dependencies list, defined in the `pyproject.toml` `[project.optional-dependencies]` section,
e.g. given a list of opt. dependencies named `test`:
`pip install -e ./package_dir_name/[test]`


## pytest debugging flags

* `-lf / --last-failed` - Runs just the tests that failed last
* `-ff / --failed-first` - Runs all the tests, starting with the last failed
* `-x / --exitfirst` - Stops the tests session after the first failure
* `--maxfail=num` - Stops the tests after num failures
* `-nf / --new-first` - Runs all the tests, ordered by file modification time
* `--sw / --stepwise` - Stops the tests at the first failure. Starts the tests at the last failure next time
* `--sw-skip / --stepwise-skip` - Same as --sw, but skips the first failure

Control pytest values:
* `-v / --verbose` - Displays all the test names, passing or failing
* `--tb=[auto/long/short/line/native/no]` - Controls the traceback style
* `-l / --showlocals` - Displays local variables alongside the stacktrace

Flags to start a command-line debugger:
* `--pdb` - Starts an interactive debugging session at the point of failure
* `--trace` - Starts the pdb source-code debugger immediately when running each test
* `--pdbcls` - Uses alternatives to pdb, such as IPython’s debugger with --pdb-cls=IPython.terminal.debugger:TerminalPdb


## tox debugging

To be able to start `pdb` when running `tox` it's necessary to make sure that we can pass
arguments through tox to pytest. This is done with `{posargs}` given to tox.ini `commands`:
```ini
commands =
  pytest --cov=cards --cov=tests --cov-fail-under=100 {posargs}
```

Then run tox by passing the `--pdb` argument (passed through to `pytest`):
`tox -e py310 -- --pdb --no-cov`
