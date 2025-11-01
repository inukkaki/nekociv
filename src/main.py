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
    cell = field.cells[7][7]
    for n in cell.neighborhood:
        rect = [2*n.pos[0], 2*n.pos[1], 2, 2]
        pygame.draw.rect(window, [255, 0, 0], rect)
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
