import ctypes
import random
import time

import numpy as np
import pygame
import pygame.locals

from src.field import (
    CELL_COORD_SCALE,
    CELL_DISTANCE,
)
from src.field.field import Field


def render_rect(surface, row, col, color):
    rect = [2*col, 2*row, 2.0, 2.0]
    pygame.draw.rect(surface, color, rect)


if __name__ == "__main__":
    # For high DPI (Windows)
    try:
        user32 = ctypes.windll.user32
        user32.SetProcessDPIAware()
    except Exception:
        pass

    pygame.init()

    # Window
    window = pygame.display.set_mode(size=(1025, 514))

    # Field
    field = Field()

    # Cell
    ship = field.cells[230][0]
    target = CELL_COORD_SCALE*np.array([200, 0], dtype=np.float64)

    # Main loop
    running = True

    while running:
        # Poll events
        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                running = False
        if not running:
            break

        # Simulation
        dists = []
        for neighbor in ship.neighborhood + [ship]:
            x_dist_1, y_dist = target - neighbor.coord
            x_dist_2 = x_dist_1 - field.width
            x_dist = min(abs(x_dist_1), abs(x_dist_2))
            dist = x_dist**2 + y_dist**2
            dists.append((dist, neighbor))
        _, ship_next = min(dists, key=lambda x: x[0])

        if ship_next == ship or np.linalg.norm(target - ship_next.coord) < 0.0:
            while True:
                target = np.array([random.random() for _ in range(2)]) - 0.5
                target_norm = np.linalg.norm(target)
                if target_norm > 0.0:
                    break
            target *= CELL_DISTANCE*random.uniform(1.0, 10.0)/target_norm
            target += ship_next.coord
        ship = ship_next

        # Render the surface
        window.fill([0, 0, 0])
        render_rect(window, ship.row, ship.col, [255, 255, 255])
        pygame.draw.circle(window, [255, 0, 0], 2*target/CELL_COORD_SCALE, 2.0)
        pygame.display.update()

        time.sleep(0.0167)
