import itertools

import pygame


def render_cell(surface, cell):
    color = [
        255*cell.pos[0]*cell.pos[1]/64, 0,
        255 - 255*cell.pos[0]*cell.pos[1]/64]
    rect = [2*cell.pos[0], 2*cell.pos[1], 2, 2]
    pygame.draw.rect(surface, color, rect)


def render_field(surface, field):
    for cell in itertools.chain.from_iterable(field.cells):
        render_cell(surface, cell)
