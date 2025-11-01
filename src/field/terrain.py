"""Module for terrain generation."""

import random

ELEV_GEN_N = -1.2  # North end
ELEV_GEN_S = -1.2  # South end

ELEV_GEN_MEAN = 0.0
ELEV_GEN_SD = 1.0

ELEV_GEN_COMPLEXITY = 1.0


def generate_terrain(field, seed):
    """Generates terrain on a field.

    Args:
        field (src.field.field.Field): Field to generate terrain on.
        seed (int): Seed value for terrain generation.
    """
    random.seed(seed)
    calc_elevs(field)


def create_close_list(field):
    """Creates a close list that is referred while terrain generation.

    Args:
        field (src.field.field.Field): Field to generate terrain on.

    Returns:
        list[list[bool]]: Close list. All values in it are `False`.
    """
    close_list = []
    for _ in range(field.height):
        temp_close_list = []
        for _ in range(field.width):
            temp_close_list.append(False)
        close_list.append(temp_close_list)
    return close_list


def calc_elevs(field):
    """Calculates cells' elevation on a field.

    Args:
        field (src.field.field.Field): Field to generate terrain on.
    """
    close_list = create_close_list(field)
    init_elevs(field, close_list)
    interpolate_elevs(field, close_list)


def init_elevs(field, close_list):
    """Initializes cells' elevation on a field.

    Args:
        field (src.field.field.Field): Field to generate terrain on.
        close_list (list[list[bool]]): Close list.
    """
    for i in range(field.height):
        for j in range(field.width):
            cell = field.cells[i][j]
            initial_cell = (
                (cell.row % field.scale == 0)
                and (cell.col % field.scale
                        == ((cell.row//field.scale) % 2)*field.scale//2))
            if cell.row == 0:
                # North end
                cell.elev = ELEV_GEN_N
                close_list[i][j] = True
            elif cell.row == field.height - 1:
                # South end
                cell.elev = ELEV_GEN_S
                close_list[i][j] = True
            elif initial_cell:
                # Cells that have an initial elevation
                cell.elev = random.gauss(ELEV_GEN_MEAN, ELEV_GEN_SD)
                close_list[i][j] = True


def interpolate_elevs_horizontally(field, close_list, scale, complexity):
    """Interpolates cells' elevation on a field horizontally.

    Args:
        field (src.field.field.Field): Field to generate terrain on.
        close_list (list[list[bool]]): Close list.
        scale (int): Interpolation scale.
        complexity (float): Elevation complexity.
    """
    for i in range(0, field.height, scale):
        for j in range(0, field.width, scale//2):
            if close_list[i][j]:
                continue
            cell = field.cells[i][j]
            r, c = cell.row, cell.col
            ref_cell_1 = field.cells[r][(c - scale//2) % field.width]
            ref_cell_2 = field.cells[r][(c + scale//2) % field.width]
            cell.elev = (ref_cell_1.elev + ref_cell_2.elev)/2
            cell.elev += random.gauss(0.0, complexity)
            close_list[i][j] = True


def interpolate_elevs_vertically_nw_se(field, close_list, scale, complexity):
    """Interpolates cells' elevation on a field vertically.

    This function refers to the elevation of a north-west cell and a south-east
    cell.

    Args:
        field (src.field.field.Field): Field to generate terrain on.
        close_list (list[list[bool]]): Close list.
        scale (int): Interpolation scale.
        complexity (float): Elevation complexity.
    """
    for i in range(scale//2, field.height, scale):
        j_start = (2*((i//scale) % 2) + 1)*scale//4
        for j in range(j_start, field.width, scale):
            if close_list[i][j]:
                continue
            cell = field.cells[i][j]
            r, c = cell.row, cell.col
            ref_cell_1 = field.cells[r - scale//2][c - scale//4]
            ref_cell_2 = \
                field.cells[r + scale//2][(c + scale//4) % field.width]
            cell.elev = (ref_cell_1.elev + ref_cell_2.elev)/2
            cell.elev += random.gauss(0.0, complexity)
            close_list[i][j] = True


def interpolate_elevs_vertically_ne_sw(field, close_list, scale, complexity):
    """Interpolates cells' elevation on a field vertically.

    This function refers to the elevation of a north-east cell and a south-west
    cell.

    Args:
        field (src.field.field.Field): Field to generate terrain on.
        close_list (list[list[bool]]): Close list.
        scale (int): Interpolation scale.
        complexity (float): Elevation complexity.
    """
    for i in range(scale//2, field.height, scale):
        j_start = (3 - 2*((i//scale) % 2))*scale//4
        for j in range(j_start, field.width, scale):
            if close_list[i][j]:
                continue
            cell = field.cells[i][j]
            r, c = cell.row, cell.col
            ref_cell_1 = \
                field.cells[r - scale//2][(c + scale//4) % field.width]
            ref_cell_2 = field.cells[r + scale//2][c - scale//4]
            cell.elev = (ref_cell_1.elev + ref_cell_2.elev)/2
            cell.elev += random.gauss(0.0, complexity)
            close_list[i][j] = True


def interpolate_elevs(field, close_list):
    """Interpolates cells' elevation on a field.

    Args:
        field (src.field.field.Field): Field to generate terrain on.
        close_list (list[list[bool]]): Close list.
    """
    scale = field.scale
    complexity = ELEV_GEN_COMPLEXITY
    while scale > 1:
        interpolate_elevs_horizontally(field, close_list, scale, complexity)
        interpolate_elevs_vertically_nw_se(
            field, close_list, scale, complexity)
        interpolate_elevs_vertically_ne_sw(
            field, close_list, scale, complexity)
        scale //= 2
        complexity /= 2
