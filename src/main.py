import time

import pygame
import pygame.locals

from src.field.field import Field
from src.field.render import render_field


def main():
    pygame.init()

    # Window
    window = pygame.display.set_mode(size=(512, 512))
    pygame.display.set_caption(title="nekociv")

    # Field
    field = Field(8, 8)
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
