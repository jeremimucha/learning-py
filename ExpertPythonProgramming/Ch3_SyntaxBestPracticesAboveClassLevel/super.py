#! /usr/bin/env python3

'''
Python `super` class is used to access the base class of a class.
'''

# The 'old way' was to call the parrent class directly, and pass an object - `self` explicitly
class OldBase:
    def dostuff(self):
        print('base doing stuff')

class OldDerived(OldBase):
    def dostuff(self):
        OldBase.dostuff(self)
        print('derived doing more stuff')

oldway = OldDerived()
oldway.dostuff()

# Using `super`

class Base:
    def dostuff(self):
        print('base doing stuff')

class Derived(Base):
    def dostuff(self):
        super(Derived, self).dostuff()      # calls Base.dostuff(self)
        print('Derived doing more stuff')

class ShorterDerived(Base):
    def dostuff(self):
        super().dostuff()                   # calls Base.dostuff(self) - implicit arguments
        print('ShorterDerived doing stuff with shorter syntax')

# The shorter form is allowed within methods - the arguments are implicit.
# `super` can be used anywhere, but arguments are required outside of a method

sd = ShorterDerived()
super(sd.__class__, sd).dostuff()   # prints 'base doing stuff'


# The second argument is also optional, when omitted `super` returns an unbounded type,
# this is usefull for class methods
class Pizza:
    def __init__(self, toppings):
        self.toppings = toppings

    def __repr__(self):
        return "Pizza with {}".format(' and '.join(self.toppings))

    @classmethod
    def recommend(cls):
        '''Recommend some pizza with arbitrary toppings,'''
        return cls(['spam', 'ham', 'eggs'])

class VikingPizza(Pizza):
    @classmethod
    def recommend(cls):
        '''Use same recommendation as super but add extra spam'''
        recommended = super(VikingPizza).recommend()    # calls Pizza.recommend()
        recommended.toppings += ['spam']*5
        return recommended

# for methods decorated with @classmethod `super` with no arguments is the same as
# `super` with one argument
