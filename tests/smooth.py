import math
import random
import time

import pygame
import pygame.locals

SCALE = 64
BASE_WIDTH = 4


def generate_terrain(scale, base_width, seed):
    width = scale*base_width + 1
    elevs = [0.0 for _ in range(width)]
    random.seed(seed)
    calc_elevs(elevs, scale, width)
    return elevs, width


def calc_elevs(elevs, scale, width):
    init_elevs(elevs, scale, width)
    interpolate_elevs(elevs, scale, width)


def init_elevs(elevs, scale, width):
    for i in range(len(elevs)):
        if i == 0 or i == width - 1:
            elevs[i] = -1.2
        elif i % scale == 0:
            elevs[i] = random.gauss(0.0, 1.0)
        else:
            elevs[i] = 0.0


def interpolate_elevs(elevs, scale, width):
    s = scale
    c = 1.0
    while s > 1:
        for i in range(s//2, width, s):
            elevs[i] = (elevs[i - s//2] + elevs[i + s//2])/2
            elevs[i] += random.gauss(0.0, c)
        s //= 2
        c /= 2


def smooth_elevs(elevs, width, filter):
    new_elevs = []
    for i in range(width):
        elev = filter(elevs, i, width)
        new_elevs.append(elev)
    return new_elevs


def render_elevs(surface, elevs):
    surface.fill([255, 255, 255])
    pygame.draw.line(surface, [128, 128, 255], (0, 256), (1024, 256))
    for i in range(len(elevs) - 1):
        y1 = -75*elevs[i] + 256
        y2 = -75*elevs[i + 1] + 256
        pygame.draw.line(surface, [0, 0, 0], (4*i, y1), (4*(i + 1), y2))


def main():
    pygame.init()

    # Window
    window = pygame.display.set_mode(size=(1030, 512))

    # Elevs
    elevs, width = generate_terrain(SCALE, BASE_WIDTH, 2)

    # Filters
    def smoothing_filter(elevs, i, width, size):
        elev = 0.0
        count = 0
        for j in range(-(size//2), size//2 + 1):
            k = i + j
            if 0 <= k and k <= width - 1:
                elev += elevs[k]
                count += 1
        elev /= count
        return elev

    def gauss(x, sigma):
        return 1/math.sqrt(2*math.pi)/sigma*math.exp(-x**2/(2*sigma**2))

    def gaussian_filter(elevs, i, width, size, sigma):
        elev = 0.0
        for j in range(-(size//2), size//2 + 1):
            k = i + j
            if 0 <= k and k <= width - 1:
                elev += elevs[k]*gauss(j, sigma)
        return elev

    def weight_filter(elevs, i, width, size):
        refs = []
        weights = []
        for j in range(-(size//2), size//2 + 1):
            k = i + j
            if 0 <= k and k <= width - 1:
                refs.append(elevs[k])
                weight_dist = 1/(i**2 + 0.001)
                weight_elev = 1/((elevs[k] - elevs[i])**2 + 0.001)
                weight = weight_dist*weight_elev
                weights.append(weight)
        weights = [w/sum(weights) for w in weights]
        elev = 0.0
        for r, w in zip(refs, weights):
            elev += r*w
        return elev

    def sharp_filter(elevs, i, width):
        elev = elevs[i]
        if i - 1 >= 0:
            elev += -elevs[i - 1]
            elev += elevs[i]
        if i + 1 <= width - 1:
            elev += -elevs[i + 1]
            elev += elevs[i]
        return elev

    # Main loop
    running = True

    while running:
        # Poll events
        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                key = event.key
                if key == pygame.K_z:
                    elevs = smooth_elevs(elevs, width, sharp_filter)
                if key == pygame.K_x:
                    elevs = smooth_elevs(
                        elevs, width, lambda elevs, i, width:
                            smoothing_filter(elevs, i, width, 3))
                if key == pygame.K_c:
                    elevs = smooth_elevs(
                        elevs, width, lambda elevs, i, width:
                            weight_filter(elevs, i, width, 3))
        if not running:
            break

        render_elevs(window, elevs)
        pygame.display.update()

        time.sleep(1/60)

    pygame.quit()


main()
