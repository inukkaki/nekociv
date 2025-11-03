import time

import pygame
import pygame.locals

from src.civ.render import render_tribe
from src.civ.tribe import Tribe
from src.field.field import Field
from src.field.render import (
    calc_elev_color,
    calc_stpn_color,
    render_field,
)
from src.field.terrain import generate_terrain


def main():
    pygame.init()

    # Window
    window = pygame.display.set_mode(size=(524, 524))
    pygame.display.set_caption(title="nekociv")

    # Field
    field = Field(64, 4, 4)
    seed = 9
    generate_terrain(field, seed)

    field_surface = pygame.Surface(size=(513, 512), flags=pygame.SRCALPHA)
    render_field(field_surface, field, calc_elev_color)
    window.blit(field_surface, (0, 0))

    # Tribe
    tribe = Tribe(50, field.cells[70][200])

    tribe_surface = pygame.Surface(size=(513, 512), flags=pygame.SRCALPHA)
    render_tribe(tribe_surface, tribe)
    window.blit(tribe_surface, (0, 0))
    pygame.display.update()

    # Main loop
    running = True

    while running:
        # Poll events
        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                running = False
        if not running:
            break

        time.sleep(1/60)

    pygame.quit()


main()
