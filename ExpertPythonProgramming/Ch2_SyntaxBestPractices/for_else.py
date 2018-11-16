#! /usr/bin/env python3

'''
The python `for` loop has an optional `else` block that's executed only if the loop ended
naturally, i.e. without terminating with the `break` statement
'''

for number in range(1):
    break
else:
    print('break')

for number in range(1):
    pass
else:
    print('no-break')
