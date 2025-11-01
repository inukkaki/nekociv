"""Module for visualizing a simulation field."""

import itertools

import pygame


def render_cell(surface, cell):
    """Renders a cell on a surface.

    Args:
        surface (pygame.Surface): Surface to render the cell.
        cell (src.field.cell.Cell): Cell to render.
    """
    c = 255*(min(max(-3.0, cell.elev), 3.0) + 3.0)/6.0
    color = [c, c, c]
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
