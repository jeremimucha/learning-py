#! usr/bin/env python3

'''
decorators can be used for checking / validating arguments that a function recieves
and returns. And example designed wiht XML-RPC protocol in mind (XML remote procedure call).
'''

rpc_info = {}

def xmlrpc(in_=(), out=(type(None),)):
    def _xmlrpc(function):
        # registering the signature
        func_name = function.__name__
        rpc_info[func_name] = (in_, out)
        def _check_types(elements, types):
            '''Subfunction that checks the types.'''
            if len(elements) != len(types):
                raise TypeError('argument count is wrong')
            for index, couple in enumerate(zip(elements, types)):
                arg, of_the_right_type = couple
                if isinstance(arg, of_the_right_type):
                    continue
                raise TypeError('arg #{} should be {}'.format(index, of_the_right_type))

        # wrapped function
        def __xmlrpc(*args):    # no keywords allowed
            # checking what goes in
            checkable_args = args[1:]   # remove self
            _check_types(checkable_args, in_)
            # running the function
            res = function(*args)
            # checking what goes out
            if not type(res) in (tuple, list):
                checkable_res = (res,)
            else:
                checkable_res = res
            _check_types(checkable_res, out)
            # the function and the type checking succeeded
            return res
        return __xmlrpc
    return _xmlrpc
# The decorator registers each function into the global dictionary and keeps a list of the types
# for its arguments and for the returned values.


class RpcView:
    @xmlrpc((int,int))          # function taking two ints returning None
    def meth1(self, int1, int2):
        print('received {} and {}'.format(int1, int2))

    @xmlrpc((str,), (int,))     # string -> int
    def meth2(self, phrase):
        print('received {}'.format(phrase))
        return 12

print(rpc_info)
rv = RpcView()
rv.meth1(1, 2)
try:
    rv.meth2(2)
except TypeError as e:
    print('Caught {}'.format(repr(e)))
