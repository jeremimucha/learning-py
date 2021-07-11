# Performance considerations in python


Rules for writing performant code:

1. Know the built-in data structures and how to use them,
2. Prefer to use built-ins whenever possible,
3. Profile! Use the cProfile module to profile the code and find bottlenecks
`python3 -m cProfile myscript.py`
