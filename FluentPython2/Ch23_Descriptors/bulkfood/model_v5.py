import abc

class Validated(abc.ABC):

    def __set_name__(self, owner, name):
        self.storage_name = name

    def __set__(self, instance, value):
        # delegates validation to the `validate` method
        value = self.validate(self.storage_name, value)
        # then uses the returned `value` to update the stored value.
        instance.__dict__[self.storage_name] = value

    @abc.abstractmethod
    # `validate` is an abstract method; this is the template method.
    def validate(self, name, value):
        """return validated value or raise ValueError"""


class Quantity(Validated):
    """a number greater than zero"""

    # Implementation fo the template method required by the
    # Validated.validate abstract method.
    def validate(self, name, value):
        if value <= 0:
            raise ValueError(f'{name} must be > 0')
        return value


class NonBlank(Validated):
    """a string with at least one non-space character"""

    def validate(self, name, value):
        value = value.strip()
        # If nothing is left after leading and trailing blanks
        # are stripped, reject the value.
        if not value:
            raise ValueError(f'{name} cannot be blank')
        # Requiring the concrete `validate` methods to return
        # the validated value gives them an opportuynity to clean up,
        # convert, or normalize the data received.
        # In this case, `value` is returned without leading or trailing blanks.
        return value
