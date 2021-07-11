# Testing python code using pytest

To run a test file with pytest:
`$ pytest -v test_true.py`

Run on an entire directory, optionally with a filter
`$ pytest -v tests -k test_fail`    # execute only tests named `test_fail`

Executes only tests marked with @pytest.mark.dicttest, the `dicttest` is an arbitrary label.
`$ pytest -v tests -m dicttest`

Skips the `dicttest` marked tests
`$ pytest -v tests -m 'not dicttest'`

Spin multiple jobs in parallel:
`$ pytest -n 4 ...`


Run with code-coverage report generation
`$ pytest --cov=some-module --cov-report=html ./some-module/tests`
