# Project distribution / installation

There are multiple tools available for the task in python:
* distutils - the oldest and "standard" one (used natively by python)
* setuptools - the "defacto-standard"
* distlib - up and comming, might replace setuptools in the future


# setuptools
* use setup.py and setup.cfg pair to configure the project distribution,
* package the project by running
  `python setup.py bdist_wheel` - for distribution for use
  `python setup.py sdist`       - source distribution


# Local, test-pypi server setup
* edit the `~/.pypirc`:
[distutils]
index-servers =
  testpypi
[testpypi]
username = jamcodes
password = 1234
repository = https://testpypi.python.org/pypi
* register the project
`python setup.py register -r testpypi`
* upload the distribution
`python setup.py sdist upload -r testpypi`
or
`python setup.py bdist_wheel upload -r testpypi`


# Using console-scripts
Distributed by setuptools into runnable locations, without the need to write custom,
portable scripts.
