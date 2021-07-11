# Python documentation using Sphinx

## Install and initial preparations
`pip install sphinx`
Once installed, run the following in the top-level directory:
`sphinx-quickstart doc` - creates directory structure expected by sphinx in the `doc` directory,
along with initial configuration.
After that the documentation can be built using
`sphinx-build`
or using the generated Makefile by running
`make [builder]`
where `[builder]` is one of the supported builders - html, latex, linkcheck.

* Enable autodoc by adding the following to `conf.py`
extensions = ['sphinx.ext.autodoc']
* Enable the autodoc actually documenting the modules automatically:
.. automodule:: foobar
    :members:
    :undoc­members:
    :show­inheritance:

Python documentation is written using reST (reStructuredText) files.
See `http://docutils.sourceforge.net/docs/ref/rst/restructuredtext.html` for reference
on how to write reStructured text.


If you have doctests-compatible examples in your documentation you can use doctests to validate them
`$ sphinx-build -b doctest doc/source doc/build`
