'''
The abstract factory pattern is used when there are multiple possible
implementations of a system, that depend on some configuration or platform.
The callin code requests an object from the abstract factory, not knowing
exactlly what class of object will be returned.
'''


# The following example is a set of formatters depending on locale
class FranceDateFormatter:
    def format_date(self, y, m, d):
        y, m, d = (str(x) for x in (y,m,d))
        y = '20' + y if len(y) == 2 else y
        m = '0' + m if len(m) == 1 else m
        d = '0' + d if len(d) == 1 else d
        return("{0}/{1}/{2}".format(d,m,y))


class USADateFormatter:
    def format_date(self, y, m, d):
        y, m, d = (str(x) for x in (y,m,d))
        y = '20' + y if len(y) == 2 else y
        m = '0' + m if len(m) == 1 else m
        d = '0' + d if len(d) == 1 else d
        return("{0}-{1}-{2}".format(m,d,y))


class FranceCurrencyFormatter:
    def format_currency(self, base, cents):
        base, cents = (str(x) for x in (base, cents))
        if len(cents) == 0:
            cents = '00'
        elif len(cents) == 1:
            cents = '0' + cents
        digits = []
        for i,c in enumerate(reversed(base)):
            if i and not i % 3:
              digits.append(' ')
            digits.append(c)
        base = ''.join(reversed(digits))
        return "{0}€{1}".format(base, cents)


class USACurrencyFormatter:
    def format_currency(self, base, cents):
    base, cents = (str(x) for x in (base, cents))
    if len(cents) == 0:
        cents = '00'
    elif len(cents) == 1:
      cents = '0' + cents
    digits = []
    for i,c in enumerate(reversed(base)):
        if i and not i % 3:
            digits.append(',')
        digits.append(c)
    base = ''.join(reversed(digits))
    return "${0}.{1}".format(base, cents)


# Having set up the formatters, now we just need to create formatter factories
class USAFormatterFactory:
    def create_date_formatter(self):
        return USADateFormatter()
    def create_currency_formatter(self):
        return USACurrencyFormatter


class FranceFormatterFactory:
    def create_date_formatter(self):
        return FranceDateFormatter()
    def create_currency_formatter(self):
        return FranceCurrencyFormatter()


factory_map = {
    'US': USAFormatterFactory,
    'FR': FranceFormatterFactory
}


if __name__ == '__main__':
    country_code = 'US'
    formatter_factory = factory_map.get(country_code)()
