# Thirdparty pytest plugins


Search for plugins here:
* https://pypi.org (search for pytest-)
* https://github.com/pytest-dev
* https://docs.pytest.org/en/latest/how-to/plugins.html
* https://docs.pytest.org/en/latest/reference/plugin_list.html


## Noteworthy plugins

* pytest-order - Allows us to specify the order using a marker
* pytest-randomly - Randomizes the order, first by file, then by class, then by test
* pytest-repeat - Makes it easy to repeat a single test, or multiple tests, a
  specific number of times
* pytest-rerunfailures - Re-runs failed tests. Helpful for flaky tests
* pytest-xdist - Runs tests in parallel, either using multiple CPUs on one
  machine, or multiple remote machines

* pytest-instafail - Adds an --instafail flag that reports tracebacks and output
  from failed tests right after the failure. Normally, pytest reports tracebacks
  and output from failed tests after all tests have completed.
* pytest-sugar - Shows green checkmarks instead of dots for passing tests
  and has a nice progress bar. It also shows failures instantly, like pytest-instafail.
* pytest-html - Allows for html report generation. Reports can be extended
  with extra data and images, such as screenshots of failure cases.

* Faker - Generates fake data for you. Provides faker fixture for use with pytest
* model-bakery - Generates Django model objects with fake data.
* pytest-factoryboy - Includes fixtures for Factory Boy, a database model data generator
* pytest-mimesis - Generates fake data similar to Faker, but Mimesis is quite a bit faster

* pytest-cov - Runs coverage while testing
* pytest-benchmark - Runs benchmark timing on code within tests
* pytest-timeout - Doesn’t let tests run too long
* pytest-asyncio - Tests async functions
* pytest-bdd - Writes behavior-driven development (BDD)–style tests with pytest
* pytest-freezegun - Freezes time so that any code that reads the time will get
  the same value during a test. You can also set a particular date or time.
* pytest-mock - A thin-wrapper around the unittest.mock patching API

Web-dev plugins
* pytest-selenium - Provides fixtures to allow for easy configuration of browser-
  based tests. Selenium is a popular tool for browser testing.
* pytest-splinter - Built on top of Selenium as a higher level interface, this
  allows Splinter to be used more easily from pytest.
* pytest-django and pytest-flask - Help make testing Django and Flask applica-
  tions easier with pytest. Django and Flask are two of the most popular
  web frameworks for Python.