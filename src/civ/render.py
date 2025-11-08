"""Module for rendering civilization systems."""

import matplotlib.cm as cm
import numpy as np
import pygame

from src.field.render import calc_cell_rect

RENDER_POPL_MAX = 100


def calc_popl_color(tribe):
    """Calculates the rendering color based on a tribe's population.

    Args:
        tribe (src.civ.tribe.Tribe): Tribe to render.

    Returns:
        out (np.ndarray): Color vector (RGBA).
    """
    x = max(0, min(tribe.popl, RENDER_POPL_MAX))/RENDER_POPL_MAX
    color = 255.0*np.array(cm.viridis(x), dtype=np.float64)
    return color


def render_tribe(surface, tribe, alpha):
    """Renders a tribe on a surface.

    If the population of the tribe is 0 or less, this function does not render
    the tribe.

    Args:
        surface (pygame.Surface): Surface to render the cell.
        tribe (src.civ.tribe.Tribe): Tribe to render.
        alpha (float): Alpha value. 0 is transparent, and 255 is fully opaque.
    """
    if not tribe.alive:
        return
    color = calc_popl_color(tribe)
    color[3] = alpha
    rect = calc_cell_rect(tribe.cell)
    pygame.draw.rect(surface, color, rect)
