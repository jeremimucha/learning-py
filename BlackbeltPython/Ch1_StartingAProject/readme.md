# Python project layout

Preffer the project layout presented here.
Most notably:
* setup.py, setup.cfg, README.rst at the top-level
* docs directory at the top level - processed with Sphinx
* module directory (here foobar) containing the module sources and tests directory.
  Note the tests directory is at the module level - not root dir.
* etc dir - at the top level - sample config files
* tools - shell scripts and related tools,
* bin - for binaries, binary scripts meant to be installed with setup.py
