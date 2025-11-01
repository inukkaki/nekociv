"""Hexagonal cells that compose a field."""

import numpy as np


class Cell:
    def __init__(self, row, col):
        self.row = row
        self.col = col

        self.pos = np.array(
            [self.col + (self.row % 2)/2, self.row], dtype=np.float64)
                # Position
