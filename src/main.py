import random
import time

import pygame
import pygame.locals

from src.civ.group import Group
from src.civ.render import (
    calc_character_color,
    calc_diff_color,
    calc_popl_color,
    render_group,
)
from src.field.field import Field
from src.field.render import (
    calc_elev_color,
    calc_elev_color_simple,
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
    render_field(field_surface, field, calc_elev_color_simple)

    # Group
    character = [0.5, 0.5, 0.5]
    groups = [
        Group(10, 20, character, field.cells[69][199]),
        Group(10, 20, character, field.cells[69][200]),
        Group(10, 20, character, field.cells[70][199]),
        Group(10, 20, character, field.cells[70][200]),
        Group(10, 20, character, field.cells[70][201]),
        Group(10, 20, character, field.cells[71][199]),
        Group(10, 20, character, field.cells[71][200]),
    ]

    group_surface = pygame.Surface(size=(513, 512), flags=pygame.SRCALPHA)
    group_color_func = calc_character_color

    # Main loop
    sim_seed = 10
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
        group_surface.fill([0, 0, 0, 0])

        groups_next = []
        for group in groups:
            new_group = group.update()
            if group.alive:
                groups_next.append(group)
                render_group(group_surface, group, group_color_func)
            if new_group != None and new_group.alive:
                groups_next.append(new_group)
                render_group(group_surface, new_group, group_color_func)
        groups = groups_next
        groups.sort(key=lambda group: group.popl)
            # Groups act in order of population size, starting with the
            # smallest

        # Update the window
        window.blit(field_surface, (0, 0))
        window.blit(group_surface, (0, 0))
        pygame.display.update()

        time.sleep(1/60)

    pygame.quit()


main()
