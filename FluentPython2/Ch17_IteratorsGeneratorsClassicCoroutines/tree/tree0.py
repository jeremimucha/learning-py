#!/usr/bin/env python3

# The `yield from` expression can be used to iterate tree structures.
# This first "baby step" just yields the name of the root class and stops.


def tree(cls):
    yield cls.__name__

def display(cls):
    for cls_name in tree(cls):
        print(cls_name)



if __name__ == '__main__':
    display(BaseException)
