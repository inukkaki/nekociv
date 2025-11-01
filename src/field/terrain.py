"""Module for terrain generation."""

import random

ELEV_GEN_MEAN = 0.0
ELEV_GEN_SD = 1.0


def generate_terrain(field, seed):
    """Generates terrain on a field.

    Args:
        field (src.field.field.Field): Field to generate terrain on.
        seed (int): Seed value for terrain generation.
    """
    random.seed(seed)
    calc_elevs(field)


def calc_elevs(field):
    """Calculates every cell's elevation on a field.

    Args:
        field (src.field.field.Field): Field to generate terrain on.
    """
    init_elevs(field)


def init_elevs(field):
    """Initializes every cell's elevation on a field.

    Args:
        field (src.field.field.Field): Field to generate terrain on.
    """
    for i in range(field.height):
        for j in range(field.width):
            cell = field.cells[i][j]
            initial_cell = (
                (cell.row % field.scale == 0)
                and (cell.col % field.scale
                        == ((cell.row//field.scale) % 2)*field.scale//2))
            if initial_cell:
                # Cells that have an initial elevation
                cell.elev = random.gauss(ELEV_GEN_MEAN, ELEV_GEN_SD)
