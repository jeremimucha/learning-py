#! /usr/bin/env python3

'''
All python3 buildins and user classes, that have no explicit parent class specified inherit from
an `object` base class. Inheriting from buildin types is fine:
'''

class DistinctError(ValueError):
    '''Raised when duplicate value is added to a distinctdict.'''

class distinctdict(dict):
    '''Dictionary that does not accept duplicate values.'''
    def __setitem__(self, key, value):
        if value in self.values():
            if (key in self.keys() and self[key] != value) or key not in self:
                raise DistinctError('This value already exists for different key')
        super().__setitem__(key, value)

mydict = distinctdict()
mydict['key'] = 'value'
try:
    mydict['other_key'] = 'value'
except Exception as e:
    print('Exception: {}'.format(e))
mydict['other_key'] = 'value2'

for k, v in mydict.items():
    print("{}: {}".format(k,v))


'''
When implementing classes it's worth considering if the design doesn't overlap in functionality
with a built-in. For example classes that work with sequences can be implemented in tearms of
a `list` to manage the sequence
'''

class Folder(list):
    def __init__(self, name):
        self.name = name

    def dir(self, nesting=0):
        offset = " " * nesting
        print("{offset}{name}/".format(offset=offset, name=self.name))

        for element in self:
            if hasattr(element, 'dir'):
                element.dir(nesting + 1)
            else:
                print("{offset} {element}".format(offset=offset, element=element))

tree = Folder('project')
tree.append('README.md')
tree.dir()
src = Folder('src')
src.append('script.py')
tree.append(src)
tree.dir()
