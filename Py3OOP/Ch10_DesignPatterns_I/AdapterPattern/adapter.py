'''
The adapter pattern is used when a class with a certain public interface
needs to be called with a different interface.
This comes into play when we have a library, which code we can not change -
we can than write an adapter class that will call the library class internally
'''
import datetime

# Some class with bad interface
class AgeCalculator:

    def __init__(self, birthday):
        self.year, self.month, self.day = (int(x) for x in birthday.split('-'))

    def calculate_age(self, date):
        year, month, day = (int(x) for x in date.split('-'))
        age = year - self.year
        if (month, day) < (self.month, self.day):
            age -= 1
        return age


# Adaptor class to the AgeCalculator
class DateAgeAdapter:
    @staticmethod
    def _str_date(date):
        return date.strftime("%Y-%m-%d")

    def __init__(self, birthday):
        birthday = DateAgeAdapter._str_date(birthday)
        self.calculator = AgeCalculator(birthday)

    def get_age(self, date):
        date = DateAgeAdapter._str_date(date)
        return self.calculator.calculate_age(date)
