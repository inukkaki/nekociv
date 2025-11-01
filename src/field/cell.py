"""Hexagonal Cells that compose a Field."""


class Cell:
    def __init__(self, row, col):
        self.row = row
        self.col = col

        self.x = self.col + (self.row % 2)/2
        self.y = self.row
