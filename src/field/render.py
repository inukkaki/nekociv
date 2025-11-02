"""Module for visualizing a simulation field."""

import itertools
import math

import numpy as np
import pygame

from src.field import (
    ELEV_SD,
    SEA_LEVEL,
)
from src.field.cell import Cell

RENDER_ELEV_SEA_COLOR_DEEP = 7.0
RENDER_ELEV_SEA_COLOR_SHALLOW = 23.0

RENDER_ELEV_MIN = -4000.0  # m
RENDER_ELEV_MAX = 4000.0   # m

RENDER_ELEV_TONE_WIDTH = 500.0  # m

RENDER_ELEV_LAND_MAX_STEP = (
    (RENDER_ELEV_MAX - RENDER_ELEV_MIN)/RENDER_ELEV_TONE_WIDTH)

RENDER_ELEV_LAND_COLOR_MIN = 47.0
RENDER_ELEV_LAND_COLOR_MAX = 255.0


def calc_elev_sea_color(elev):
    """Calculates the rendering color based on a sea cell's elevation.

    Args:
        elev (float): Elevation of the cell which surface is sea.

    Returns:
        float: Monochrome color level.
    """
    if elev < SEA_LEVEL - ELEV_SD:
        c = RENDER_ELEV_SEA_COLOR_DEEP
    else:
        c = RENDER_ELEV_SEA_COLOR_SHALLOW
    return c


def calc_elev_land_color(elev):
    """Calculates the rendering color based on a land cell's elevation.

    Args:
        elev (float): Elevation of the cell which surface is land.

    Returns:
        float: Monochrome color level.
    """
    if elev < RENDER_ELEV_MIN:
        c = RENDER_ELEV_LAND_COLOR_MIN
    elif RENDER_ELEV_MAX < elev:
        c = RENDER_ELEV_LAND_COLOR_MAX
    else:
        step = (elev - RENDER_ELEV_MIN)//RENDER_ELEV_TONE_WIDTH
        c = float(int(
            (RENDER_ELEV_LAND_COLOR_MAX - RENDER_ELEV_LAND_COLOR_MIN)
            /math.pow(RENDER_ELEV_LAND_MAX_STEP, 3)*math.pow(step, 3)
                + RENDER_ELEV_LAND_COLOR_MIN))
    return c


def calc_elev_color(cell):
    """Calculates the rendering color based on a cell's elevation.

    Args:
        cell (src.field.cell.Cell): Cell to render.

    Returns:
        np.ndarray: Color vector (RGBA).
    """
    if cell.surface == Cell.SURFACE_SEA:
        c = calc_elev_sea_color(cell.elev)
    elif cell.surface == Cell.SURFACE_LAND:
        c = calc_elev_land_color(cell.elev)
    else:
        c = 0.0
    color = np.array([c, c, c, 255.0], dtype=np.float64)
    return color


def render_cell(surface, cell):
    """Renders a cell on a surface.

    Args:
        surface (pygame.Surface): Surface to render the cell.
        cell (src.field.cell.Cell): Cell to render.
    """
    color = calc_elev_color(cell)
    rect = [2*cell.pos[0], 2*cell.pos[1], 2, 2]
    pygame.draw.rect(surface, color, rect)


def render_field(surface, field):
    """Renders a field on a surface.

    Args:
        surface (pygame.Surface): Surface to render the field.
        field (src.field.field.Field): Field to render.
    """
    for cell in itertools.chain.from_iterable(field.cells):
        render_cell(surface, cell)
