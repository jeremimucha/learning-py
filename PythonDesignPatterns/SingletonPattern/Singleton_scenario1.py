#! python3

'''
A practical use case to implement a consistent database operations.
Multiple callers acces a single database instance
'''

import sqlite3


class MetaSingleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class Database(metaclass=MetaSingleton):
    _connection = None
    def connect(self):
        if self._connection is None:
            self._connection = sqlite3.connect('db.sqlite3')
            self._cursorobj = self._connection.cursor()
        return self._cursorobj

db1 = Database().connect()
db2 = Database().connect()

print("Database Objects DB1", db1)
print("Database Objects DB2", db2)
