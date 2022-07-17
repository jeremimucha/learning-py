# Patametrization

Using pytest we can parameterize tests the following ways:
* function parametrization,
* fixture parametrization,
* pytest_generate_test hook,


## Running subsets of test cases

Given a large number of generated test cases we might want to run
only a subset of them. This is done using the `-k` flag

- run only cases containing `todo` parameters
  `pytest -v -k todo`
- run only cases containing `todo` but not `play` or `create`
  `pytest -v -k "todo and not (play or create)`

It's generally a good idea to quote the argument specifying the
test case we want to run, to avoid any shell parsing misshaps
`pytest -v "test_finish_param::test_finish[write a book-done]"`
