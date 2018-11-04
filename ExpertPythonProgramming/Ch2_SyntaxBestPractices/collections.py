#! /usr/bin/env python3


# list
# -------------------------------------------------------------------------------------------------
# - implemented as a variable lenght array - a vector, rather than a linked list,
# This has the same implications that a std::vector carries - operations at the and of the
# structure as well as random access are cheap, however inserting/deleting at an arbitrary
# position has O(n) complexity.
print('--- list ---')
lst = [1,2,3,4]
print('type: ', type(lst))
print(lst)
lst.append(5)       # O(1) == push_back()
elem = lst[3]       # O(1) == operator[]
last = lst.pop()    # O(1) default .pop() == pop_back()
lst.extend((9,8,7)) # O(k), where k = number of element pushed back to the list
len(lst)            # O(1)

# use collections.deque for a container with amortized constant time operations at front and back

# list idioms:

# use list comprehensions whenever possible to avoid raw loops
even = [i for i in range(10) if i % 2 == 0]

# use enumerate() if element indices are needed:
for i, elem in enumerate(['one', 'two', 'three', 'four']):
    print(i, elem)

# use zip() to aggregate multiple iterables of the same length,
# a common patter is to uniformly iterate over two same-sized iterables:
for item in zip([1,2,3], [4,5,6]):
    print(item)

# calling zip() on a result of zip() reverses the result...
for item in zip(*zip([1,2,3], [4,5,6])):    # *zip() unpacks the iterable
    print(item)

# unpacking allows for capturing multiple elements in a single variable using starred expression
# as long as it is unambiguous
first, second, *rest = 0, 1, 2, 3, 4
print('first: {}, second: {}, rest: {}'.format(first, second, rest))

first, *inner, last = 0, 1, 2, 3, 4
print('first: {}, inner: {}, last: {}'.format(first, inner, last))
print('--- list end ---')
# -------------------------------------------------------------------------------------------------


# dict - unordered_map / hash map
# -------------------------------------------------------------------------------------------------
print('--- dict ---')

d = {1: ' one', 2: ' two', 3: ' three'}
print(d)

# dict comprehension
squares = {number: number**2 for number in range(10)}
print(squares)

# iteration methods
# - keys()   : This returns the dict_keys object that provides a view on all the keys
# - values() : This returns the dict_values object that provides views on all the values
# - items()  : This returns the dict_items object providing views on all (key, value) tuples
# Those methods return a 'view' object - same as a range of iterators or a span from C++
# This means that the views reflect the changes that happen to the dictionary
words = {'foo': 'bar', 'fizz': 'bazz'}
items = words.items()
words['spam'] = 'eggs'
print(items)

# use OrderedDict from collections if it's important that the order of additions is preserved
from collections import OrderedDict
od = OrderedDict( (str(number), None) for number in range(5) )
print(od)
print(od.keys())

print('--- dict end---')
# -------------------------------------------------------------------------------------------------


# set
# -------------------------------------------------------------------------------------------------
print('--- set ---')
# set() - mutable
# frozenset() - immutable, and therefore hashable - can be used in dicts or sets

# construction:
s0 = set([0,1,2])
s1 = {elem for elem in range(3)}
s2 = {1, 2, 3}
empty_set = set()   # note that {} is an empty dictionary

print('--- set end ---')
# -------------------------------------------------------------------------------------------------


# other important containers from the `collections` module
# - namedtuple() : This is a factory function for creating tuple subclasses whose indexes can be
#   accessed as named attributes
# - deque : This is a double-ended queue, list-like generalization of stacks and queues with fast
#   appends and pops on both ends
# - ChainMap : This is a dictionary-like class to create a single view of multiple mappings
# - Counter : This is a dictionary subclass for counting hashable objects
# - OrderedDict : This is a dictionary subclass that preserves the order the entries were added in
# - defaultdict : This is a dictionary subclass that can supply missing values
#   with a provided default
