"""Module for a simulation field."""

from src.field.cell import Cell


class Field:
    """Field where simulations are performed on.

    Attributes:
        width (int): Number of rows in the cell array.
        height (int): Number of columns in the cell array.
        cells (list[list[src.field.cell.Cell]]): 2D array of cells.
    """

    def __init__(self, width, height):
        """Field where simulations are performed on.

        Args:
            width (int): Number of rows in the cell array.
            height (int): Number of columns in the cell array.
        """
        self.width = width
        self.height = height

        self.cells = []
        for row in range(self.height):
            temp_cells = []
            for col in range(self.width):
                cell = Cell(row, col)
                temp_cells.append(cell)
            self.cells.append(temp_cells)
