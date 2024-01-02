#!/usr/bin/env python3
from dataclasses import dataclass, field

@dataclass
class Cell:
    value: int = None

class Board:
    size: int = 9

    def __init__(self, cells=None, size=9):
        """Populate cells of the board by string.

        Uses right-to-left order, ignoring all characters
        but the numbers and emptychar.
        """
        self.size = size
        self.cells = list(cells)
        # TODO: malformed board check
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
