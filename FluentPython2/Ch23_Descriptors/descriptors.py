#!/usr/bin/env python3


# A descriptor is a class implementing one or more of:
#   __get__
#   __set__
#   __delete__
# methods. Descriptor is used by declaring instances of it
# as class attributes of another class.
#
# Descriptor class
#   A class implementing the descriptor protocol
#
# Managed class
#   The class where the descriptor instances are declared as class attributes.
#
# Descriptor instance
#   Class attributes of a managed class bound to instances of a Descriptor class.
#
# Managed instance
#   Instance of the managed class.
#
# Storage attribute
#   Attribute of the managed instance that holds the value of a managed attribute
#   for that particular instance.
#
# Managed attribute
#   A public attribute in the managed class that is handled by a descriptor instance,
#   with values stored in storage attrbiutes. In other words, a descriptor instance and
#   a storage attribute provide the infrastructure for a managed attribute.


# Descriptor rules

# Use `property` to keep it simple
#
# For most use cases prefer to use `@property` instead of creating descriptors implementing
# both __set__ and __get__, even if you don't need a setter - the default will raise AttributeError.

# Read-only descriptors require __set__
#
# When using descriptors to implement a read-only attribute, you must provide both __get__ and __set__.
# Otherwise setting a namesake attribute on an instance will shadow the descriptor.
# The __set__ of a read-only should raise AttributeError.

# Validation descriptors can work with __set__ only
#
# In a descriptor designed only for validation, the __set__ method should check
# the value argument it gets, and if valid, set it directly in the instance __dict__
# using the descriptor instance name as key. That wa, reading the attribute with
# the same name from the instance will be as fast as possible, because it will not
# require a __get__.

# Caching can be done efficiently with __get__ only
#
# Coding just the __get__ method gives us a nonoverriding descriptor.
# These are useful to make some expensive computation and then cache the result by setting
# an attribute by the same name on the instance. The namesake instance attribute will shadow
# the descriptor, so subsequent access to that attribute will fetch it directly from the instance
# __dict__ and not trigger the descriptor __get__ anymore. The @functools.cached_property
# decorator actually produces a nonoverriding descriptor.

if __name__ == '__main__':
    pass
