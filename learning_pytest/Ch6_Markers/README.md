# pytest markers


Markers are used to tag (or mark) test cases, to describe or modify their behavior.

* `@pytest.mark.filterwarnings(warning)`  - adds a warning filter to the given test
* `@pytest.mark.skip(reason=None)`    - skips the test with optional reason
* `@pytest.mark.skipif(condition, ..., *, reason)` - skip the test if any of the conditions are true
* `@pytest.mark.xfail(condition, ..., *reason, run=True, raises=None, strict=xfail_strict)`
  Tells pytest that the given test is expected to fail
* `@pytest.mark.parametrize(argname, argvalues, indirect, ids, scope)`
  Parametrizes a test case
* `@pytest.mark.usefixtures(fixturename1, fixturename2, ...)`
  Marks test as needing all the specified fixtures


## Custom markers

We can define markers ourselves - to tag/label test cases
Custom markers need to be registered in pytest.ini

Run tests based on markers:

- run only tests marked `exception`
  `pytest -v -m exception`
- run only  tests marked `smoke`
  `pytest -v -m smoke`


Run `pytest --markers` to list all markers
