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
    field = Field()
    field_seed = 9  # 3, 9
    generate_terrain(field, field_seed)

    field_sfc_1 = pygame.Surface(size=(1025, 514), flags=pygame.SRCALPHA)
    field_sfc_2 = pygame.Surface(size=(1025, 514), flags=pygame.SRCALPHA)
    render_field(field_sfc_1, field, calc_elev_color)
    render_field(field_sfc_2, field, calc_elev_color_simple)

    # Group
    groups = []

    central_cell = field.cells[80][200]
    character = [0.5, 0.5, 0.5]
    groups.append(Group(10, 20, character, central_cell))
    for neighbor in central_cell.neighborhood:
        groups.append(Group(10, 20, character, neighbor))

    """
    central_cell = field.cells[80][320]
    character = [0.5, 0.5, 1.0]
    groups.append(Group(10, 20, character, central_cell))
    for neighbor in central_cell.neighborhood:
        groups.append(Group(10, 20, character, neighbor))
    """

    popl_sfc = pygame.Surface(size=(1025, 514), flags=pygame.SRCALPHA)
    char_sfc = pygame.Surface(size=(1025, 514), flags=pygame.SRCALPHA)

    # Main loop
    sim_seed = 1
    random.seed(sim_seed)

    m_pressing = False
    m_x0, m_y0 = pygame.mouse.get_pos()
    m_x1, m_y1 = m_x0, m_y0
    m_wh = 0

    major_sfc = pygame.Surface(size=(1025, 514), flags=pygame.SRCALPHA)
    cam_ax, cam_ay = 1025/2, 514/2
    cam_x, cam_y = 0, 0
    cam_scale = 1.0

    running = True

    while running:
        # Poll events
        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    cam_x = 0
                    cam_y = 0
                    cam_scale = 1.0
            elif event.type == pygame.MOUSEBUTTONDOWN:
                m_pressing = True
            elif event.type == pygame.MOUSEBUTTONUP:
                m_pressing = False
            elif event.type == pygame.MOUSEWHEEL:
                m_wh = event.y
        if not running:
            break

        m_x1, m_y1 = pygame.mouse.get_pos()
        if m_pressing:
            m_dx = m_x1 - m_x0
            m_dy = m_y1 - m_y0
            cam_x += m_dx/cam_scale
            cam_y += m_dy/cam_scale
        m_x0, m_y0 = m_x1, m_y1
        cam_scale *= 1.0 + 0.1*m_wh
        m_wh = 0

        # Simulation
        #popl_sfc.fill([0, 0, 0, 0])
        char_sfc.fill([0, 0, 0, 0])

        groups_next = []
        for group in groups:
            new_group = group.update()
            if group.alive:
                groups_next.append(group)
            if new_group != None and new_group.alive:
                groups_next.append(new_group)
        groups = groups_next
        groups.sort(key=lambda group: group.popl)
            # Groups act in order of population size, starting with the
            # smallest

        for group in groups:
            #render_group(popl_sfc, group, calc_popl_color)
            render_group(char_sfc, group, calc_character_color)

        # Update the window
        window.fill([0, 0, 0])

        window.blit(pygame.transform.scale(field_sfc_1, (512, 257)), (0, 514))
        #window.blit(pygame.transform.scale(popl_sfc, (512, 257)), (0, 514))

        major_sfc.blit(field_sfc_2, (0, 0))
        major_sfc.blit(char_sfc, (0, 0))

        dst_x = cam_scale*(cam_x - cam_ax) + cam_ax
        dst_y = cam_scale*(cam_y - cam_ay) + cam_ay
        dst_w = cam_scale*1025
        dst_h = cam_scale*514

        window.blit(
            pygame.transform.scale(major_sfc, (dst_w, dst_h)), (dst_x, dst_y))

        pygame.display.update()

        time.sleep(1/60)

    pygame.quit()


main()
