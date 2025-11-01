from src.field.field import Field


def main():
    field = Field(8, 8)
    for temp_cells in field.cells:
        for cell in temp_cells:
            print(f"{cell.pos}", end=" ")
        print()


main()
