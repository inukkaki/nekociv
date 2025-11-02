"""Module for tribes."""


class Tribe:
    """Tribe that has a population of 1 or more.

    Attributes:
        popl (int): Population. If this value is 0 or less, this tribe will
            perish.
        cell (src.field.cell.Cell): Cell which this tribe exists on.
    """

    def __init__(self, popl, cell):
        """Tribe that has a population of 1 or more.

        Args:
            popl (int): Population.
            cell (src.field.cell.Cell): Cell which this tribe exists on.
        """
        self.popl = popl

        self.cell = cell
        self.cell.tribe = self

    def perish(self):
        """Eliminates this tribe from the cell if the population is 0 or less.
        """
        if self.popl <= 0:
            self.cell.tribe = None
