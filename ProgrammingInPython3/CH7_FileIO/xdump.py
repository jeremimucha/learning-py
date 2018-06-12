#! python3

import struct
import os

b =  bytearray(open('BRF_testfile.txt', 'rb').read())
for i in b:
    print(i, end=' ')
for lino, record in enumerate(struct.iter_unpack('<15s', b), start=1):
    print('{0}: {1}'.format(lino, record[0]), encoding=None)
