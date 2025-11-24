import ctypes
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
    # For high DPI (Windows)
    try:
        user32 = ctypes.windll.user32
        user32.SetProcessDPIAware()
    except Exception:
        pass

    pygame.init()

    # Window
    window = pygame.display.set_mode(size=(1025, 771))
    pygame.display.set_caption(title="nekociv")

    # Field
    field = Field(64, 8, 4)
    field_seed = 9  # 3, 9
    generate_terrain(field, field_seed)

    field_sfc_1 = pygame.Surface(size=(1025, 514), flags=pygame.SRCALPHA)
    field_sfc_2 = pygame.Surface(size=(1025, 514), flags=pygame.SRCALPHA)
    render_field(field_sfc_1, field, calc_stpn_color)
    render_field(field_sfc_2, field, calc_elev_color)

    # Group
    character = [0.5, 0.5, 0.5]
    groups = [
        Group(10, 20, character, field.cells[79][199]),
        Group(10, 20, character, field.cells[79][200]),
        Group(10, 20, character, field.cells[80][199]),
        Group(10, 20, character, field.cells[80][200]),
        Group(10, 20, character, field.cells[80][201]),
        Group(10, 20, character, field.cells[81][199]),
        Group(10, 20, character, field.cells[81][200]),
    ]

    popl_sfc = pygame.Surface(size=(1025, 514), flags=pygame.SRCALPHA)
    char_sfc = pygame.Surface(size=(1025, 514), flags=pygame.SRCALPHA)

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
        #popl_sfc.fill([0, 0, 0, 0])
        char_sfc.fill([0, 0, 0, 0])

        groups_next = []
        for group in groups:
            new_group = group.update()
            if group.alive:
                groups_next.append(group)

                #render_group(popl_sfc, group, calc_popl_color)
                render_group(char_sfc, group, calc_character_color)
            if new_group != None and new_group.alive:
                groups_next.append(new_group)

                #render_group(popl_sfc, new_group, calc_popl_color)
                render_group(char_sfc, new_group, calc_character_color)
        groups = groups_next
        groups.sort(key=lambda group: group.popl)
            # Groups act in order of population size, starting with the
            # smallest

        # Update the window
        window.blit(pygame.transform.scale(field_sfc_1, (512, 257)), (0, 514))
        #window.blit(pygame.transform.scale(popl_sfc, (512, 257)), (0, 514))

        window.blit(field_sfc_2, (0, 0))
        window.blit(char_sfc, (0, 0))

        pygame.display.update()

        time.sleep(1/60)

    pygame.quit()


main()
