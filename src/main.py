import random
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

    # Tribe
    tribes = [
        Tribe(10, 20, field.cells[69][199]),
        Tribe(10, 20, field.cells[69][200]),
        Tribe(10, 20, field.cells[70][199]),
        Tribe(10, 20, field.cells[70][200]),
        Tribe(10, 20, field.cells[70][201]),
        Tribe(10, 20, field.cells[71][199]),
        Tribe(10, 20, field.cells[71][200]),
    ]

    tribe_surface = pygame.Surface(size=(513, 512), flags=pygame.SRCALPHA)

    # Main loop
    sim_seed = 1
    random.seed(sim_seed)

    running = True

    while running:
        # Poll events
        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                running = False
        if not running:
            break

        # Simulation
        tribe_surface.fill([0, 0, 0, 0])

        tribes_next = []
        for tribe in tribes:
            tribe.update()
            if tribe.alive:
                tribes_next.append(tribe)

            render_tribe(tribe_surface, tribe)
        tribes = tribes_next

        # Update the window
        window.blit(field_surface, (0, 0))
        window.blit(tribe_surface, (0, 0))
        pygame.display.update()

        time.sleep(1/60)

    pygame.quit()


main()
