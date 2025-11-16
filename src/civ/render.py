"""Module for rendering civilization systems."""

import matplotlib.cm as cm
import numpy as np
import pygame

from src.field.render import calc_cell_rect

RENDER_POPL_MAX = 250
RENDER_DIFF_MAX = 5.0


def calc_popl_color(group):
    """Calculates the rendering color based on a group's population.

    Args:
        group (src.civ.group.Group): Group to render.

    Returns:
        out (np.ndarray): Color vector (RGBA).
    """
    x = max(0, min(group.popl, RENDER_POPL_MAX))/RENDER_POPL_MAX
    color = 255.0*np.array(cm.viridis(x), dtype=np.float64)
    return color


def calc_diff_color(group):
    """Calculates the rendering color based on a group's difficulty.

    Args:
        group (src.civ.group.Group): Group to render.

    Returns:
        out (np.ndarray): Color vector (RGBA).
    """
    x = max(0, min(group.diff, RENDER_DIFF_MAX))/RENDER_DIFF_MAX
    color = 255.0*np.array(cm.viridis(x), dtype=np.float64)
    return color


def calc_character_color(group):
    """Calculates the rendering color based on a group's character.

    Args:
        group (src.civ.group.Group): Group to render.

    Returns:
        out (np.ndarray): Color vector (RGBA).
    """
    color = 255.0*group.character
    return color


def render_group(surface, group, color_func):
    """Renders a group on a surface.

    If the population of the group is 0 or less, this function does not render
    the group.

    Args:
        surface (pygame.Surface): Surface to render the cell.
        group (src.civ.group.Group): Group to render.
        color_func (Callable[src.civ.group.Group, numpy.ndarray]): Function to
            calculate the rendering color.
    """
    if not group.alive:
        return
    color = color_func(group)
    rect = calc_cell_rect(group.cell)
    pygame.draw.rect(surface, color, rect)
