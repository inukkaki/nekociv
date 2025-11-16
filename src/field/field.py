"""Module for a simulation field."""

import itertools

from src.field.cell import Cell


class Field:
    """Field which simulations are performed on.

    Attributes:
        scale (int): Scale of terrain simplicity. The greater this value is,
            the simpler the terrain becomes.
        width (int): Number of rows in the cell array.
        height (int): Number of columns in the cell array.
        cells (list[list[src.field.cell.Cell]]): 2D array of cells.
        cell_diameter (float): Diameter of a circle inscribed in a cell.
    """
    CIRCUMFERENCE = 40_000  # km

    def __init__(self, scale, base_width, base_height):
        """Field which simulations are performed on.

        Args:
            scale (int): Scale of terrain simplicity. The greater this value
                is, the simpler the terrain becomes.
            base_width (int): This value, multiplied by the scale, becomes the
                width of this field.
            base_height (int): This value, multiplied by the scale and added 1,
                becomes the height of this field.
        """
        self.scale = scale
        self.width = self.scale*base_width
        self.height = self.scale*base_height + 1

        self.cells = []
        for row in range(self.height):
            temp_cells = []
            for col in range(self.width):
                cell = Cell(row, col)
                temp_cells.append(cell)
            self.cells.append(temp_cells)
        self.init_neighborhood_of_cells()

        self.cell_diameter = 1000*Field.CIRCUMFERENCE/(2*self.height)  # m

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
