#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""

"""

import sys

class IterBetter:
    """
    Returns an object that can be used as an iterator
    but can also be used via __getitem__ (although it
    cannot go backwards -- that is, you cannot request
    `iterbetter[0]` after requesting `iterbetter[1]`).

    It is also possible to get the first value of the iterator or None.

    For boolean test, IterBetter peeps at first value in the iterator without effecting the iteration.
    """
    def __init__(self, iterator):
        self.i, self.c = iterator, 0

    def first(self, default=None):
        """
        Returns the first element of the iterator or None when there are no elements.

        If the optional argument default is specified, that is returned instead
        of None when there are no elements.
        """
        try:
            return next(iter(self))
        except StopIteration:
            return default

    def __iter__(self):
        if hasattr(self, "_head"):
            yield self._head

        while 1:
            try:
                yield next(self.i)
            except StopIteration:
                return
            self.c += 1

    def __getitem__(self, i):
        # todo: slices
        if i < self.c:
            raise IndexError("already passed " + str(i))
        try:
            while i > self.c:
                next(self.i)
                self.c += 1
            # now self.c == i
            self.c += 1
            return next(self.i)
        except StopIteration:
            raise IndexError(str(i))

    def __nonzero__(self):
        if hasattr(self, "__len__"):
            return self.__len__() != 0
        elif hasattr(self, "_head"):
            return True
        else:
            try:
                self._head = next(self.i)
            except StopIteration:
                return False
            else:
                return True

    __bool__ = __nonzero__

iterbetter = IterBetter

if __name__ == "__main__":
    c = iterbetter(iter(range(5)))
    print(c.first())
    print(c[0])
    print(c.first())
    print(c.first())
    print(c.first())
    # ci = iter(c)
    # print(next(ci))
