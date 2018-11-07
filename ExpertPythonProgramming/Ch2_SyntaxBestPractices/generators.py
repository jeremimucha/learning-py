#! usr/bin/env python3

'''
Generators - based on the `yield` statement. They allow to pause a function and return an
intermediate result.
'''
def fibonacci():
    a, b = 0 ,1
    while True:
        yield b
        a, b = b, a + b

# Generators can be treated like iterators. We can call next() on them or use them in a loop
fib = fibonacci()
print(next(fib))
print(next(fib))
lst = [next(fib) for i in range(5)]
print(lst)
for i, k in zip(range(5), fib):
    print(i, k)


'''
Always consider generators when processing elements in a loop/chain/stream.
Example - apply a chain of operations to each element:
'''
def power(values):
    for value in values:
        print("powering {} ".format(value))
        yield value

def adder(values):
    for value in values:
        print("adding to {} ".format(value))
        if value % 2 == 0:
            yield value + 3
        else:
            yield value + 2

elements = [1,4,7,9,12,19]
results = adder(power(elements))
print(next(results))
print(next(results))
for i in results:
    print(i)

'''
Python's `yield` statement can also be used as an expression allowing us to `.send` a value
into the generator function.
'''
def psychologist():
    print('Please tell me your problems')
    while True:
# It's done by assining the value yield expression returns to a variable.
        answer = (yield)
        if answer is not None:
            if answer.endswith('?'):
                print("Don't ask yourself too much questions")
            elif 'good' in answer:
                print("Ahh that's good, go on")
            elif 'bad' in answer:
                print("Don't be so negative")

free = psychologist()
'''We must prime the generator by calling `next` once - to make sure the generator code reaches
the `(yield)` expression.'''
next(free)
free.send('I feel bad')
free.send("Why I shouldn't?")
free.send("Ok then I should find what is good for me")
'''
`.send` acts like next, but also makes `yield` return the value passed to it inside of the
function definition. This lets generator take client code input.
Two other methods complement this behavior.
`throw` - lets client code send any exception to be raised
`close` - sends a `GeneratorExit` exception - generator must reraise it or raise StopIteration
'''
