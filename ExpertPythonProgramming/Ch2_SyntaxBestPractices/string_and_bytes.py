#! /usr/bin/env python3


print("--- str ---")
# In python3 `str` literals are unicode
print('type: ', type("some string"))
# This means that the string is "abstract" and independent of the underlying representation.
# To convert a string into a byte sequence they must be encoded to binary data:
test_str = 'źć - some string - ąę'
print('.encode()', test_str.encode('utf-8', 'strict') )
# Alternatively a bytes() constructor can be used
print('bytes(): ', bytes(test_str, 'utf-8', 'strict') )
print("-----------\n")


# Raw bytes - unsigned ints in range [0, 256) - are represented by:
# - bytes() - immutable
# - bytearray() - mutable
# They can be converted to strings in the analogous ways - by decoding the binary representation
# to unicode:

print("--- bytes ---")
test_bytes = b'some bytes'
print('type: ', type(test_bytes))
print('.decode(): ', test_bytes.decode('utf-8', 'strict') )
print('str(): ', str(test_bytes, 'utf-8', 'strict') )
print("-------------")

# bytearray() is mutable - can be changed in place, indexed, appended, pop'ed, inserted etc.
print("--- bytearray ---")
test_ba = bytearray(b'some bytearray')
print('type: ', type(test_ba))
print('.decode(): ', test_ba.decode('utf-8', 'strict'))
test_ba[:4] = b'mutated'
print('test_ba[:4] = b"mutated": ', test_ba)
print("-----------------")
