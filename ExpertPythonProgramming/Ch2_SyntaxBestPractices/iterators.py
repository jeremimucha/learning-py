#! /usr/bin/env python3

'''
An iterator is a container object that implement the iterator protocol.
It's base on two methods:
* __next__ : returns the next item of the container
* __iter__ : returns the iterator itself
'''

# The `iter()` build in function creates iterators from sequences.
# When the sequence is exhaused a `StopIteration` exception is raised.
i = iter('abc')
try:
    print(next(i))
    print(next(i))
    print(next(i))
    print(next(i))
except StopIteration as e:
    print("StopIterator exception caught: ", repr(e))


# Implementing a custom iterator - __next__ must be implemented for the iterator object,
# StopIteration should be raised to indicate end of sequence.
# __iter__() must return the iterator itself
class CountDown:
    def __init__(self, step):
        self.step = step
    def __next__(self):
        '''Return the next element.'''
        if self.step <= 0:
            raise StopIteration
        self.step -= 1
        return self.step
    def __iter__(self):
        '''Return the iterator itself'''
        return self

print("for loop over CountDown(4):")
for element in CountDown(4):
    print(element)

