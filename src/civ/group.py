"""Module for groups."""

import random

from src import EPSILON
from src.field.cell import Cell


class Group:
    """Group that has a population of 1 or more.

    Attributes:
        popl (int): Population. If this value is 0 or less, this group will
            perish.
        food (int): Number of food.
        diff (float): Difficulty.
        popl_decr (int): Population decline from this group (Popl. decrement).
            This is used as a temporary variable, and will always be 0 before
            `update()` is executed.
        popl_emig (int): Population migrating from this group (Popl.
            emigrants). This is used as a temporary variable, and will always
            be 0 before `update()` is executed.
        cell (src.field.cell.Cell): Cell that this group exists on.
        alive (bool): Indicates if this group is alive.
    """
    POPL_INCR_MAX = 3

    POPL_DECR_PROB = 0.2
    POPL_DECR_MAX = 5

    DIFF_INIT = 1.0
    DIFF_COMMON_RATIO_INCR = 1.05
    DIFF_COMMON_RATIO_DECR = 0.95
    DIFF_COMMON_RATIO_SETL = 1.025

    FOOD_PROD_PARAM = 1000.0

    EMIG_DEST_WEIGHT_PARAM = 0.001

    def __init__(self, popl, food, cell):
        """Group that has a population of 1 or more.

        Args:
            popl (int): Population.
            food (int): Number of food.
            cell (src.field.cell.Cell): Cell which this group exists on.
        """
        self.popl = popl
        self.food = food
        self.diff = Group.DIFF_INIT

        self.popl_decr = 0
        self.popl_emig = 0

        self.cell = cell
        self.cell.group = self

        self.alive = True

    def consume_food(self):
        """Consumes food and causes population change."""
        consumption = self.popl
        self.food -= consumption

        if self.food > 0:
            if self.popl >= 2:
                # Population increase
                self.popl += random.randint(0, Group.POPL_INCR_MAX)
            self.diff *= Group.DIFF_COMMON_RATIO_INCR
        elif self.food < 0:
            # Starvation
            self.popl_decr = min(-self.food, self.popl)
            self.food = 0
            self.diff *= Group.DIFF_COMMON_RATIO_DECR
        else:
            # Natural decline in population
            if random.random() < Group.POPL_DECR_PROB:
                self.popl_decr = min(
                    random.randint(0, Group.POPL_DECR_MAX), self.popl)

            # Difficulty increase due to settlement
            self.diff *= Group.DIFF_COMMON_RATIO_SETL

    def select_dest_for_emig(self):
        """Selects the destination for emigration from neighbor cells.

        Returns:
            out (src.field.cell.Cell | None): Destination cell if there are
                neighbor ones that can be emigrated. Otherwise, None.
        """
        dest = None
        candidates = [
            neighbor for neighbor in self.cell.neighborhood
            if neighbor.surface == Cell.SURFACE_LAND]
        if len(candidates) == 0:
            return dest
        weights = []
        for candidate in candidates:
            weight = EPSILON
            if candidate.group == None:
                weight += self.EMIG_DEST_WEIGHT_PARAM/candidate.stpn
            else:
                group = candidate.group
                weight += group.food/(group.diff*group.popl)
            weights.append(weight)
        dest = random.choices(candidates, weights=weights, k=1)[0]
        return dest

    def emigrate(self):
        """Emigrates a part of the population to a neighbor cell or group.

        Returns:
            out (src.civ.group.Group | None): New group if the emigrants move
                to a cell that no groups exist on. Otherwise, None.
        """
        new_group = None

        if self.popl_decr <= 0:
            # The population does not decrease
            return new_group
        self.popl_emig = random.randint(0, self.popl_decr)
        if self.popl_emig <= 0:
            # No one is going to emigrate
            return new_group

        dest = self.select_dest_for_emig()
        if dest == None:
            # There are no neighbor cells that can be emigrated
            return new_group

        if dest.group == None:
            # Develop a new cell
            new_group = Group(self.popl_emig, 0, dest)
            new_group.produce_food()
        else:
            # Emigrate to an existing group
            dest.group.popl += self.popl_emig

        return new_group

    def decrease_popl(self):
        """Decreases the population based on `popl_decr`."""
        self.popl -= self.popl_decr

    def produce_food(self):
        """Produces food based on the circumstances of this group."""
        if self.popl > 0:
            self.food += int(
                self.popl/(self.diff*Group.FOOD_PROD_PARAM*self.cell.stpn
                           + EPSILON))

    def perish(self):
        """Eliminates this group from the cell if the population is 0 or less.
        """
        if self.popl <= 0:
            self.cell.group = None
            self.alive = False

    def update(self):
        """Updates this group's situation.

        Returns:
            out (src.civ.group.Group | None): New group if the emigrants move
                to a cell that no groups exist on. Otherwise, None.
        """
        self.popl_decr = 0
        self.popl_emig = 0

        self.consume_food()
        new_group = self.emigrate()
        self.decrease_popl()
        self.produce_food()

        self.perish()

        return new_group
