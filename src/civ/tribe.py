"""Module for tribes."""

import random

from src import EPSILON


class Tribe:
    """Tribe that has a population of 1 or more.

    Attributes:
        popl (int): Population. If this value is 0 or less, this tribe will
            perish.
        food (int): Number of food.
        diff (float): Difficulty.
        cell (src.field.cell.Cell): Cell which this tribe exists on.
        alive (bool): Indicates if this tribe is alive.
    """
    POPL_INCR_MAX = 3

    DIFF_INIT = 1.0
    DIFF_COMMON_RATIO_INCR = 1.05
    DIFF_COMMON_RATIO_DECR = 0.90

    FOOD_PROD_PARAM = 1000.0

    def __init__(self, popl, food, cell):
        """Tribe that has a population of 1 or more.

        Args:
            popl (int): Population.
            food (int): Number of food.
            cell (src.field.cell.Cell): Cell which this tribe exists on.
        """
        self.popl = popl
        self.food = food
        self.diff = Tribe.DIFF_INIT

        self.cell = cell
        self.cell.tribe = self

        self.alive = True

    def consume_food(self):
        """Consumes food and causes population change."""
        consumption = int(self.diff*self.popl)
        self.food -= consumption
        if self.food > 0:
            if self.popl >= 2:
                self.popl += random.randint(0, Tribe.POPL_INCR_MAX)
            self.diff *= Tribe.DIFF_COMMON_RATIO_INCR
        elif self.food < 0:
            self.popl -= int(min(-self.food, self.popl))
            self.food = 0
            self.diff *= Tribe.DIFF_COMMON_RATIO_DECR

    def produce_food(self):
        """Produces food based on the circumstances of this tribe."""
        self.food += int(
            self.popl/(Tribe.FOOD_PROD_PARAM*self.cell.stpn + EPSILON))

    def perish(self):
        """Eliminates this tribe from the cell if the population is 0 or less.
        """
        if self.popl <= 0:
            self.cell.tribe = None
            self.alive = False

    def update(self):
        """Updates this tribe's situation."""
        self.consume_food()
        self.produce_food()

        self.perish()
