"""Module for cells that compose a simulation field."""

import numpy as np


class Cell:
    """Hexagonal cell that composes a field.

    Attributes:
        row (int): Row number where this cell is located on the field.
        col (int): Column number where this cell is located on the field.
        pos (numpy.ndarray): Position of this cell.
        neighborhood (list[src.field.cell.Cell]): List of neighbor cells.
        elev (float): Elevation (m).
        surface (int): State of this cell's surface.
        tribe (src.civ.tribe.Tribe): Tribe that exists on this cell.
    """
    SURFACE_SEA = 0
    SURFACE_LAND = 1

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

        self.neighborhood = []

        self.elev = 0.0  # m

        self.surface = Cell.SURFACE_SEA

        self.tribe = None
