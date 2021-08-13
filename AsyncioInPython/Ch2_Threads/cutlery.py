#! /usr/bin/env python

from attr import attrs, attrib
from threading import Lock

# Super simple "data structure" to demonstrate issues with threaded concurrency.
# Used by the ThreadBot class, which withdraws and deposits 'knives' and 'forks'.
# The implementation is not thread safe - race conditions are possible in the `change` method.
#
# The ThreadsafeCutlery class deals with the race condition issue the simplest possible way,
# by putting a lock around each `change` operation. This largely serializes all operations.

@attrs
class Cutlery:
    knives = attrib(default=0)
    forks = attrib(default=0)

    def give(self, to: 'Cutlery', knives=0, forks=0):
        self.change(-knives, -forks)
        to.change(knives, forks)

    def change(self, knives, forks):
        self.knives += knives
        self.forks += forks

    def __repr__(self):
        return 'Cutlery(knives={!r}, forks={!r})'.format(self.knives, self.forks)


class ThreadsafeCutlery(Cutlery):

    def __init__(self, knives=0, forks=0):
        super().__init__(knives, forks)
        self._lock = Lock()

    def change(self, knives, forks):
        with self._lock as lock:
            super().change(knives, forks)
