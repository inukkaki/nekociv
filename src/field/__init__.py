"""Modules for a simulation field and terrain generation."""

import math

import numpy as np

N_DIM_FIELD = 2

FIELD_SCALE = 64
FIELD_BASE_WIDTH = 8
FIELD_BASE_HEIGHT = 4

FIELD_WIDTH = FIELD_SCALE*FIELD_BASE_WIDTH
FIELD_HEIGHT = FIELD_SCALE*FIELD_BASE_HEIGHT + 1

FIELD_CIRCUMFERENCE = 40_000  # km

CELL_DIAMETER = 1000*4/3*FIELD_CIRCUMFERENCE/(2*FIELD_HEIGHT - 1)  # m
    # Distance from the center of a (hexagonal) cell to a vertex

CELL_DISTANCE = math.sqrt(3)/2*CELL_DIAMETER  # m
    # Distance between the centers of adjacent cells

CELL_COORD_SCALE = np.array(
    [CELL_DISTANCE, 3/4*CELL_DIAMETER], dtype=np.float64)  # m

FIELD_COORD_X_MAX = CELL_DISTANCE*FIELD_WIDTH  # m

SEA_LEVEL = 0.0  # m

ELEV_MEAN = 0.0   # m
ELEV_SD = 1_000.0  # m
