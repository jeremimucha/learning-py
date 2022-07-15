# Profiling in python

## Static profiling

- https://github.com/benfred/py-spy


## Dynamic profiing

- `python3 -m cProfile <profile-target>`

```
         5677 function calls in 0.674 seconds

   Ordered by: standard name

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.001    0.001    0.468    0.468 primes_1.py:20(<listcomp>)
        1    0.002    0.002    0.674    0.674 primes_1.py:4(<module>)
     4999    0.467    0.000    0.467    0.000 primes_1.py:8(check_if_prime)
        1    0.000    0.000    0.674    0.674 {built-in method builtins.exec}
        1    0.000    0.000    0.000    0.000 {built-in method builtins.len}
      673    0.203    0.000    0.203    0.000 {built-in method builtins.print}
        1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}
```

- More verbose output:
  `python3 -m cProfile -o <output-name>.prof <profile-target>`

  Open the output in `snakeviz`


- using `line_profiler` - requires additional code instrumentation - see `primes_2.py`
  After installing `line_profiler` add `@profile` decorators to the functions
  you want profiled and execute the program:
  `kernprof -l primes_2.py`
  And analyze the results:
  `python -m line_profiler primes_2.py.lprof`
```
Timer unit: 1e-06 s

Total time: 6.65939 s
File: primes_2.py
Function: check_if_prime at line 7

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
     7                                           @profile
     8                                           def check_if_prime(number):
     9      4999       1684.9      0.3      0.0      result = True
    10
    11  12492502    3055329.1      0.2     45.9      for i in range(2, number):
    12  12487503    3592557.9      0.3     53.9          if number % i == 0:
    13     33359       8417.1      0.3      0.1              result = False
    14
    15      4999       1403.0      0.3      0.0      return result
```

  