#!/usr/bin/env python3


# Next step - the tree generator will yield the name of the root class,
# and the names of each direct subclass. The names of the subclasses
# are indented to reveal the hierarchy.


def tree(cls):
    yield cls.__name__, 0
    for sub_cls in cls.__subclasses__():
        yield sub_cls.__name__, 1

def display(cls):
    for cls_name, level in tree(cls):
        indent = ' ' * 4 * level
        print(f'{indent}{cls_name}')


if __name__ == '__main__':
    display(BaseException)
