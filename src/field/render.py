"""Module for rendering a simulation field."""

import itertools
import math

import matplotlib.cm as cm
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

RENDER_STPN_MAX = 0.005


def calc_elev_sea_color(elev):
    """Calculates the rendering color based on a sea cell's elevation.

    Args:
        elev (float): Elevation of the cell which surface is sea.

    Returns:
        out (float): Monochrome color level.
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
        out (float): Monochrome color level.
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
        out (numpy.ndarray): Color vector (RGBA).
    """
    if cell.surface == Cell.SURFACE_SEA:
        c = calc_elev_sea_color(cell.elev)
        color = np.array([c, c, c, 255.0], dtype=np.float64)
    elif cell.surface == Cell.SURFACE_LAND:
        c = calc_elev_land_color(cell.elev)
        color = np.array([c, c, c, 255.0], dtype=np.float64)
    else:
        color = np.array([255.0, 0.0, 255.0, 255.0], dtype=np.float64)
    return color


def calc_stpn_color(cell):
    """Calculates the rendering color based on a cell's steepness.

    Args:
        cell (src.field.cell.Cell): Cell to render.

    Returns:
        out (numpy.ndarray): Color vector (RGBA).
    """
    if cell.surface == Cell.SURFACE_SEA:
        c = calc_elev_sea_color(cell.elev)
        color = np.array([c, c, c, 255.0], dtype=np.float64)
    elif cell.surface == Cell.SURFACE_LAND:
        x = min(cell.stpn, RENDER_STPN_MAX)/RENDER_STPN_MAX
        color = 255.0*np.array(cm.viridis(x), dtype=np.float64)
    else:
        color = np.array([0.0, 0.0, 0.0, 255.0], dtype=np.float64)
    return color


def calc_cell_rect(cell):
    """Calculates a rect that encloses a cell's area.

    Args:
        cell (src.field.cell.Cell): Cell to render.

    Returns:
        out (list[float]): Rect that encloses the cell's area.
    """
    rect = [2*cell.pos[0], 2*cell.pos[1], 2.0, 2.0]
    return rect


def render_cell(surface, cell, color_func):
    """Renders a cell on a surface.

    Args:
        surface (pygame.Surface): Surface to render the cell.
        cell (src.field.cell.Cell): Cell to render.
        color_func (Callable[src.field.cell.Cell, numpy.ndarray]): Function to
            calculate the rendering color.
    """
    color = color_func(cell)
    rect = calc_cell_rect(cell)
    pygame.draw.rect(surface, color, rect)


def render_field(surface, field, color_func):
    """Renders a field on a surface.

    Args:
        surface (pygame.Surface): Surface to render the field.
        field (src.field.field.Field): Field to render.
        color_func (Callable[src.field.cell.Cell, numpy.ndarray]): Function to
            calculate the rendering color.
    """
    for cell in itertools.chain.from_iterable(field.cells):
        render_cell(surface, cell, color_func)
