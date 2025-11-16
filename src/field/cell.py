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
        stpn (float): Steepness. Mean elevation gradient with neighbor cells. A
            steepness of 1.0 is defined as a vertical distance of 1 meter for
            every absolute difference of elevation of 1 meter.
        surface (int): State of this cell's surface.
        group (src.civ.group.Group): Group that exists on this cell.
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
        self.stpn = 0.0

        self.surface = Cell.SURFACE_SEA

        self.group = None
