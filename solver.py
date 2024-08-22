from collections import defaultdict
from functools import cache
from itertools import chain
import math
import re
import string


def ingest(board_string):
    board_string = re.sub(r'\s', '', board_string)
    board_string = re.sub(r'\D', '0', board_string)
    if not math.sqrt(math.sqrt(len(board_string))).is_integer():
        raise ValueError('Board must have a cubic number of elements')
    return Board(int(n) for n in board_string)


def solve(board):
    # eliminate all singles until none are left
    lasthash = None
    while lasthash != (lasthash:=hash(board)):
        board.apply(*singles(board))
    # TODO: use cells_and_groups to better generate permutations
    return board


def singles(board: Board):
    """Return index, value pairs of cells that are singles."""
    # TODO: turn this generator into Board method cells_options (minus the
    # len == 1 part), then use this
    return (
        (cell, solution.pop())
        for cell, value, groups in board.cells_and_groups()
        if not value
        and len(solution := board.solved_group - set(chain(*groups))) == 1
    )

class Board(list):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        size = math.sqrt(len(self))
        house_size = math.sqrt(size)
        if not (size.is_integer() and house_size.is_integer()):
            raise ValueError('Board must be a square with square dimensions.')
        self.size = int(size)
        self.house_size = int(house_size)
        self.solved_group = set(range(1, self.size+1))
    def __hash__(self):
        return hash(tuple(self))
    def __repr__(self):
        cells = len(self)
        filled = cells - self.count(0)
        return f'<{type(self).__name__}, {filled}/{cells} filled>'
    def __str__(self):
        horizontal = '+'.join(['-'*self.house_size]*self.house_size)
        horizontal = '\n' + horizontal + '\n'
        grouper_ = lambda s: grouper(s, self.house_size)
        rows = (
            '|'.join(''.join(map(str, sub)) for sub in grouper_(row))
            for row in self.rows
        )
        return horizontal.join('\n'.join(big_row) for big_row in grouper_(rows))
    @property
    @cache
    def rows(self):
        return tuple(grouper(self, self.size))
    @property
    @cache
    def columns(self):
        return tuple(transpose(self.rows))
    @property
    def houses(self):
        return tuple(self.house_dict.values())
    @property
    def house_dict(self):
        d = defaultdict(list)
        for row, group in enumerate(self.rows):
            for column, value in enumerate(group):
                # floor of row, column divided by the house size gives groups
                d[self.house_pair(row, column)].append(value)
        return d

    def cells_and_groups(self):
        """Yield each (cell, value) paired with their three groups."""
        hs = self.house_size
        for cell, value in enumerate(self):
            row, column = divmod(cell, self.size)
            house = self.house_dict[self.house_pair(row, column)]
            row = self.rows[row]
            column = self.columns[column]
            yield cell, value, (house, row, column)

    def apply(self, *solutions):
        for cell, value in solutions:
            self[cell] = value

    def house_pair(self, row, column):
        """Return the pair characteristic of cell in row, column."""
        return row//self.house_size, column//self.house_size


def grouper(iterable, n):
    iters = [iter(iterable)] * n
    return zip(*iters)
def transpose(iterable):
    return zip(*iterable)
