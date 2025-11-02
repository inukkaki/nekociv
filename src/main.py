import time

import pygame
import pygame.locals

from src.field.field import Field
from src.field.render import render_field
from src.field.terrain import generate_terrain


def main():
    pygame.init()

    # Window
    window = pygame.display.set_mode(size=(524, 524))
    pygame.display.set_caption(title="nekociv")

    # Field
    field = Field(64, 4, 4)
    generate_terrain(field, 1)
    render_field(window, field)
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
