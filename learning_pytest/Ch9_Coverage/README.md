# Coverage in python

Coverage reports can be generated with the `coverage` python package.
`pytest-cov` helps with pytest ingeration, making use easier.

## Get coverage

Using `coverage directly`:

`coverage run --soruce=<source> -m pytest <directory>`
`coverage report`


Or relying on `pytest-cov`:

`pytest --cov=<package> directory`
e.g.
`pytest --cov=cards project`

We can get a more detailed report on the missing lines:
`pytest --cov=cards --cov-report=term-missing project`
or
`coverage report --show-missing`

A much more readable format is HTML:
`pytest --cov=cards --cov-report=html project`
or
`pytest --cov=cards project`\
`coverage html`


## Exclude lines from coverage:

This is done with `#pragma: no cover`
