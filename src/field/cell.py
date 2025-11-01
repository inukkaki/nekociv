"""Module for cells that compose a simulation field."""

import numpy as np


class Cell:
    """Hexagonal cell that composes a field.

    Attributes:
        row (int): Row number where this cell is located on the field.
        col (int): Column number where this cell is located on the field.
        pos (numpy.ndarray): Position of this cell.
    """

    def __init__(self, row, col):
        """Hexagonal cell that composes a field.

        Args:
            row (int): Row number where this cell is located on the field.
            col (int): Column number where this cell is located on the field.
        """
        self.row = row
        self.col = col

        self.pos = np.array(
            [self.col + (self.row % 2)/2, self.row], dtype=np.float64)
