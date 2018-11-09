#! usr/bin/env python3

'''
Decorators can be used for caching results of pure (in the functional sense) functions.
The decorator is used to map arguments to the result that was computed using them,
and can return the result directly on subsequent calls. This is called 'memoization'
'''

import time
import hashlib
import pickle


cache = {}

def is_obsolete(entry, duration):
    return time.time() - entry['time'] > duration

def compute_key(function, args, kw):
    key = pickle.dumps((function.__name__, args, kw))
    return hashlib.sha1(key).hexdigest()

def memoize(duration=10):
    def _memoize(function):
        def __memoize(*args, **kws):
            key = compute_key(function, args, kws)
            # do we have it already?
            if (key in cache and not is_obsolete(cache[key], duration)):
                print('we got a winner')
                return cache[key]['value']
            # computing
            result = function(*args, **kws)
            # storing the result
            cache[key] = {
                'value': result,
                'time': time.time()
            }
            return result
        return __memoize
    return _memoize


@memoize()
def very_very_complex_function(a, b):
    return a + b

very_very_complex_function(2, 2)
very_very_complex_function(2, 2)
print('cache: {}'.format(cache))
