#! python3
"""
>>> import shutil
>>> import sys

>>> S = struct.Struct("<15s")
>>> fileA = os.path.join(tempfile.gettempdir(), "fileA.dat")
>>> fileB = os.path.join(tempfile.gettempdir(), "fileB.dat")
>>> for name in (fileA, fileB):
...    try:
...        os.remove(name)
...    except EnvironmentError:
...        pass

>>> brf = BinaryRecordFile(fileA, S.size)
>>> for text in ("Alpha", "Bravo", "Charlie", "Delta",
...        "Echo", "Foxtrot", "Golf", "Hotel", "India", "Juliet",
...        "Kilo", "Lima", "Mike", "November", "Oscar", "Papa",
...        "Quebec", "Romeo", "Sierra", "Tango", "Uniform", "Victor",
...        "Whisky", "X-Ray", "Yankee", "Zulu"):
...    brf.append(S.pack(text.encode("utf8")))
>>> assert len(brf) == 26
>>> brf.append(S.pack(b"Extra at the end"))
>>> assert len(brf) == 27
>>> shutil.copy(fileA, fileB)
>>> del brf[12]
>>> del brf[0]
>>> del brf[24]
>>> assert len(brf) == 24, len(brf)
>>> brf.close()

>>> if ((os.path.getsize(fileA) + (3 * S.size)) !=
...        os.path.getsize(fileB)):
...    print("FAIL#1: expected file sizes are wrong")
...    sys.exit()

>>> shutil.copy(fileB, fileA)
>>> if os.path.getsize(fileA) != os.path.getsize(fileB):
...    print("FAIL#2: expected file sizes differ")
...    sys.exit()

>>> for name in (fileA, fileB):
...    try:
...        os.remove(name)
...    except EnvironmentError:
...        pass

"""

import os
import struct
import tempfile


class BinaryRecordFile:

    def __init__(self, filename, record_size, auto_flush=True):
        self._record_size = record_size
        mode = "w+b" if not os.path.exists(filename) else 'r+b'
        self._fh = open(filename, mode)
        self.auto_flush = auto_flush

    @property
    def record_size(self):
        return self._record_size

    @property
    def name(self):
        return self._fh.name

    def flush(self):
        '''Writes to disk. Done automatically if auto_flush is True.'''
        self._fh.flush()

    def close(self):
        self._fh.close()

    def append(self, record):
        '''Appends a new record to the end of the file'''
        assert isinstance(record, (bytes, bytearray)), 'binary data required'
        assert len(record) == self.record_size, (
            'record must be exactly {} bytes'.format(self.record_size))
        self._fh.seek(0, os.SEEK_END)
        self._fh.write(record)
        if self.auto_flush:
            self._fh.flush()

    def __setitem__(self, index, record):
        '''Sets the item at index to the given record. The index must exist
        within the current file'''
        assert isinstance(record, (bytes, bytearray)), 'binary data required'
        assert len(record) == self._record_size, (
            'record must be exactly {} bytes'.format(self._record_size))
        self._seek_to_index(index)
        self._fh.write(record)
        if self.auto_flush:
            self._fh.flush()

    def __getitem__(self, index):
        '''Returns item at the given index.
        If there is no item at the given index, raises an IndexError exception.
        '''
        self._seek_to_index(index)
        return self._fh.read(self.record_size)

    def _seek_to_index(self, index):
        if self.auto_flush:
            self._fh.flush()
        self._fh.seek(0, os.SEEK_END)
        end = self._fh.tell()
        offset = index * self.record_size
        if offset >= end:
            raise IndexError("Index position {} beyond the EOF".format(index))
        self._fh.seek(offset)

    def __delitem__(self, index):
        '''Deletes the item at the given index position.
        Moves all the subsequent records one index forward'''
        self._fh.seek(0, os.SEEK_END)
        end = self._fh.tell()
        self._seek_to_index(index)
        w = self._fh.tell()
        while self._fh.seek(w + self.record_size) and self._fh.tell() < end:
            data = self._fh.read(self._record_size)
            self._fh.seek(w)
            self._fh.write(data)
            w = self._fh.tell()
        else:
            self._fh.truncate(w)
            self._fh.flush()

    def __len__(self):
        if self.auto_flush:
            self._fh.flush()
        self._fh.seek(0, os.SEEK_END)
        end = self._fh.tell()
        return end // self.record_size

if __name__ == "__main__":
    # S = struct.Struct("<15s")
    # brf = BinaryRecordFile('BRF_testfile.txt', S.size)
    # for text in ("Alpha", "Bravo", "Charlie", "Delta",
    #        "Echo", "Foxtrot", "Golf", "Hotel", "India", "Juliet",
    #        "Kilo", "Lima", "Mike", "November", "Oscar", "Papa",
    #        "Quebec", "Romeo", "Sierra", "Tango", "Uniform", "Victor",
    #        "Whisky", "X-Ray", "Yankee", "Zulu"):
    #    brf.append(S.pack(text.encode("utf8")))
    # print(len(brf))
    # for i in range(len(brf)):
    #     print(brf[i].strip(b'\x00'))
    # del brf[25]
    # print(len(brf))
    # del brf[0]
    # del brf[0]
    # del brf[11]
    # # del brf[24]
    # print(len(brf))
    # for i in range(len(brf)):
    #     print(brf[i].strip(b'\x00'))
    # brf.append(S.pack('dupa'.encode('utf8')))
    # for i in range(len(brf)):
    #     print(brf[i].strip(b'\x00'))
    import doctest
    doctest.testmod()
