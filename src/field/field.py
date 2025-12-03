"""Module for a simulation field."""

import itertools

import numpy as np

from src.field import (
    FIELD_HEIGHT,
    FIELD_SCALE,
    FIELD_WIDTH,
)
from src.field.cell import Cell


class Field:
    """Field which simulations are performed on.

    Attributes:
        scale (int): Scale of terrain simplicity. The greater this value is,
            the simpler the terrain becomes.
        width (int): Number of rows in the cell array.
        height (int): Number of columns in the cell array.
        cells (list[list[src.field.cell.Cell]]): 2D array of cells.
    """
    RNG_SEED_MIN = 1
    RNG_SEED_MAX = 2**31 - 1

    def __init__(self):
        """Field which simulations are performed on."""
        self.scale = FIELD_SCALE
        self.width = FIELD_WIDTH
        self.height = FIELD_HEIGHT

        self.cells = []
        for row in range(self.height):
            temp_cells = []
            for col in range(self.width):
                cell = Cell(row, col)
                temp_cells.append(cell)
            self.cells.append(temp_cells)
        self.init_neighborhood_of_cells()

    def init_neighborhood_of_cells(self):
        """Initializes every cell's neighborhood."""
        for cell in itertools.chain.from_iterable(self.cells):
            cell.neighborhood.clear()
            r, c = cell.row, cell.col
            if r >= 1:
                if r % 2 == 0:
                    cell_1 = self.cells[r - 1][(c - 1) % self.width]
                    cell_2 = self.cells[r - 1][c]
                else:
                    cell_1 = self.cells[r - 1][c]
                    cell_2 = self.cells[r - 1][(c + 1) % self.width]
                cell.neighborhood.append(cell_1)
                cell.neighborhood.append(cell_2)
            cell_3 = self.cells[r][(c - 1) % self.width]
            cell_4 = self.cells[r][(c + 1) % self.width]
            cell.neighborhood.append(cell_3)
            cell.neighborhood.append(cell_4)
            if r <= self.height - 2:
                if r % 2 == 0:
                    cell_5 = self.cells[r + 1][(c - 1) % self.width]
                    cell_6 = self.cells[r + 1][c]
                else:
                    cell_5 = self.cells[r + 1][c]
                    cell_6 = self.cells[r + 1][(c + 1) % self.width]
                cell.neighborhood.append(cell_5)
                cell.neighborhood.append(cell_6)

    def init_rng_of_cells(self, seed):
        """Initializes every cell's random number generator.

        Args:
            seed (int): Seed for generating the seeds for the cells' generator.
        """
        rng = np.random.default_rng(seed)
        for cell in itertools.chain.from_iterable(self.cells):
            seed = rng.integers(Field.RNG_SEED_MIN, Field.RNG_SEED_MAX)
            cell.init_rng(seed)
