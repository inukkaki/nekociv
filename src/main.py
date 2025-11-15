import random
import time

import pygame
import pygame.locals

from src.civ.group import Group
from src.civ.render import (
    calc_diff_color,
    calc_popl_color,
    render_group,
)
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

    # Group
    groups = [
        Group(10, 20, field.cells[69][199]),
        Group(10, 20, field.cells[69][200]),
        Group(10, 20, field.cells[70][199]),
        Group(10, 20, field.cells[70][200]),
        Group(10, 20, field.cells[70][201]),
        Group(10, 20, field.cells[71][199]),
        Group(10, 20, field.cells[71][200]),
    ]

    group_surface = pygame.Surface(size=(513, 512), flags=pygame.SRCALPHA)
    group_color_func = calc_popl_color

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
        random.shuffle(groups)

        # Update the window
        fs = pygame.transform.scale(field_surface, (2*513, 2*512))
        ts = pygame.transform.scale(group_surface, (2*513, 2*512))
        window.blit(fs, (-513, 0))
        window.blit(ts, (-513, 0))
        pygame.display.update()

        time.sleep(1/60)

    pygame.quit()


main()
