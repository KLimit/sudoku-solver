#!/usr/bin/env python3
import itertools

class Cell:

    emptychar = '.'

    def __init__(self, value=None):
        self.value = value

    def __repr__(self):
        return repr(self.value or self.emptychar)


class Board:

    def __init__(self, cells=None, size=9):
        """Populate cells of the board by string.

        Uses right-to-left order, ignoring all characters
        but the numbers and emptychar.
        """
        self.size = size
        self.house_size = size ** 0.5
        if not self.house_size.is_integer():
            raise ValueError('board size must be a square number (for houses)')
        self.cells = list(cells)
        if size**2 < len(self.cells):
            raise IndexError('too many cells')
        while len(self.cells) < size**2:
            self.cells.append(Cell())

    @classmethod
    def fromstring(cls, boardstring, size=9, emptychar='.'):
        allowed = tuple(str(n) for n in range(0, size+1)) + (emptychar, )
        cells = (
            Cell(char if char != emptychar else None)
            for char in boardstring
            if char in allowed
        )
        return cls(cells, size=size)

    def rows(self):
        """Yield rows at a time."""
        # truncated from itertools' "grouper" recipe
        cells = [iter(self.cells)] * self.size
        yield from zip(*cells, strict=True)

    def columns(self):
        """Yield columns at a time."""
        key = lambda n: n[0] % self.size
        cells = sorted(enumerate(self.cells), key=key)
        for _, group in itertools.groupby(cells, key):
            yield tuple(cell for col, cell in group)

    def houses(self):
        """Yield houses at a time."""
        houses = [[] for _ in self.size]
