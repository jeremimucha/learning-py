# Example of a simple python package (module)

## Workflow

* Run `python setup.py check` to verify that the setup script is correct.
* Install the package in `develop` mode - in current environment.
  This deploys the package for development, so that any changes to the code
  will be applied directly to the package after the interpreter is restarted,
  making it easy to change and work with tests.
  
  ```bash
  python setup.py develop
  # work on the package
  # ...
  # when done:
  python setup.py develop --uninstall
  ```

* Create the package by running:
  ```bash
  # create a source distribution
  python setup.py sdist

  # create a wheel package (requires python3 -m pip install wheel first)
  python setup.py bdist_wheel
  ```

* Deploy to pypi

  - install twine: `python -m pip install twine`
  - upload the package: `python -m twine upload --repository <...> <package-dir>/*`
  - It is also possible to deploy a local pypi server:
    https://github.com/pypiserver/pypiserver
    