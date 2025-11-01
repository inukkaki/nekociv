from src.field.cell import Cell


class Field:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        # Cells
        self.cells = []
        for row in range(self.height):
            temp_cells = []
            for col in range(self.width):
                cell = Cell(row, col)
                temp_cells.append(cell)
            self.cells.append(temp_cells)
