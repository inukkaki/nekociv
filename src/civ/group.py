"""Module for groups."""

import random

import numpy as np

from src import EPSILON
from src.field import (
    CELL_DISTANCE,
    FIELD_COORD_X_MAX,
    N_DIM_FIELD,
)
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
        character (numpy.ndarray): Character. Represented as a 3D vector, and
            every element is in the range from 0.0 to 1.0.
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

    FOOD_PROD_PARAM = 1100.0

    EMIG_DEST_WEIGHT_PARAM_1 = 0.01
    EMIG_DEST_WEIGHT_PARAM_2 = 0.001

    CROS_TEMP_DEST_DIST_MIN = 10_000     # m
    CROS_TEMP_DEST_DIST_MAX = 1_000_000  # m
    CROS_TOTAL_DIST_MAX = 1_000_000      # m

    N_DIM_CHARACTER = 3
    CHAR_MIN = 0.0
    CHAR_MAX = 1.0

    CHAR_MUTATE_PARAM_1 = 0.05
    CHAR_MUTATE_PARAM_2 = 5.0
    CHAR_MUTATE_PARAM_3 = 50

    def __init__(self, popl, food, character, cell):
        """Group that has a population of 1 or more.

        Args:
            popl (int): Population.
            food (int): Number of food.
            character (list | numpy.ndarray): Character. Represented as a 3D
                vector, and every element must be in the range from 0.0 to 1.0.
            cell (src.field.cell.Cell): Cell which this group exists on.
        """
        self.popl = popl
        self.food = food
        self.diff = Group.DIFF_INIT

        self.popl_decr = 0
        self.popl_emig = 0

        self.character = np.array(character, dtype=np.float64)

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
        candidates = self.cell.neighborhood
        if len(candidates) == 0:
            return dest
        weights = []
        for candidate in candidates:
            weight = EPSILON
            if candidate.surface == Cell.SURFACE_SEA:
                weight += self.EMIG_DEST_WEIGHT_PARAM_1
            elif candidate.surface == Cell.SURFACE_LAND:
                if candidate.group == None:
                    weight += self.EMIG_DEST_WEIGHT_PARAM_2/candidate.stpn
                else:
                    group = candidate.group
                    weight += group.food/(group.diff*group.popl)
            weights.append(weight)
        dest = random.choices(candidates, weights=weights, k=1)[0]
        return dest

    def emigrate_to_empty_cell(self, dest):
        """Emigrates to a cell that no groups exist on.

        Args:
            dest (src.field.cell.Cell): Cell for the emigration destination.

        Returns:
            out (src.civ.group.Group): New group emigrated to the destination
                cell.
        """
        new_group = Group(self.popl_emig, 0, self.character, dest)
        new_group.produce_food()
        return new_group

    def emigrate_to_other_group(self, group):
        """Emigrates to an existing other group.

        In this method, the character of the group for the emigration target is
        recalculated based on the ration of its native population to immigrant
        population.

        Args:
            group (src.civ.group.Group): Group for the emigration target.
        """
        gpopl = group.popl
        group.popl += self.popl_emig

        # Blend the character of the other group and the immigrants
        ipopl = self.popl_emig  # Immigrant population
        group.character = (
            gpopl*group.character + ipopl*self.character)/(gpopl + ipopl)

    def set_temporary_dest_for_crossing(self, cell_curr):
        """Set a temporary destination cell in the route for crossing.

        Args:
            cell_curr (src.field.cell.Cell): Cell that serves as the departure
                point for the destination.

        Returns:
            out (src.field.cell.Cell): Temporary destination cell.
        """
        while True:
            direction = np.array(
                [random.random() for _ in range(N_DIM_FIELD)]) - 0.5
            direction_norm = np.linalg.norm(direction)
            if direction_norm > 0.0:
                break
        temp_dest = direction/direction_norm
        temp_dest *= random.uniform(
            Group.CROS_TEMP_DEST_DIST_MIN, Group.CROS_TEMP_DEST_DIST_MAX)
        temp_dest += cell_curr.coord
        return temp_dest

    def calc_vanish_prob_for_crossing(self, total_dist):
        """Calculate the probability of vanishing during the crossing.

        Args:
            total_dist (float): Total distance of the crossing (m).

        Returns:
            out (float): Probability of vanishing.
        """
        return 2*total_dist/Group.CROS_TOTAL_DIST_MAX**2

    def cross_sea(self, departure_cell):
        """Cross the sea and emigrate to another cell or group.

        Args:
            departure_cell (src.field.cell.Cell): Cell that serves as the
                departure point for this crossing.

        Returns:
            out (src.civ.group.Group | None): New group if the emigrants move
                to a cell that no groups exist on. Otherwise, None.
        """
        new_group = None

        # Departure
        cell_curr = departure_cell
        temp_dest = self.set_temporary_dest_for_crossing(cell_curr)
        total_dist = CELL_DISTANCE

        while total_dist < Group.CROS_TOTAL_DIST_MAX:
            # Vanish during the crossing
            vanish_prob = self.calc_vanish_prob_for_crossing(total_dist)
            if random.random() < vanish_prob:
                break

            # Determine the next cell to proceed
            candidates_and_dists = []
            candidates = [cell_curr] + cell_curr.neighborhood
            for candidate in candidates:
                x_dist_1, y_dist = temp_dest - candidate.coord
                x_dist_2 = abs(x_dist_1 - FIELD_COORD_X_MAX)
                x_dist = min(abs(x_dist_1), x_dist_2)
                dist = x_dist**2 + y_dist**2
                candidates_and_dists.append((candidate, dist))
            cell_next, dist = min(candidates_and_dists, key=lambda x: x[1])

            # Landing
            if cell_next.surface == Cell.SURFACE_LAND:
                if cell_next.group == None:
                    new_group = self.emigrate_to_empty_cell(cell_next)
                else:
                    self.emigrate_to_other_group(cell_next.group)
                break

            # Re-determine a temporary destination
            if cell_next == cell_curr or dist < CELL_DISTANCE**2:
                temp_dest = self.set_temporary_dest_for_crossing(cell_next)
            cell_curr = cell_next
            total_dist += CELL_DISTANCE

        return new_group

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

        if dest.surface == Cell.SURFACE_SEA:
            # Cross the sea
            new_group = self.cross_sea(dest)
        elif dest.surface == Cell.SURFACE_LAND:
            # Reach another cell or group
            if dest.group == None:
                new_group = self.emigrate_to_empty_cell(dest)
            else:
                self.emigrate_to_other_group(dest.group)

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

    def mutate_character(self):
        """Mutates this group's character randomly."""
        direction = np.array(
            [random.random() for _ in range(Group.N_DIM_CHARACTER)]) - 0.5
        direction_norm = np.linalg.norm(direction)
        if direction_norm <= 0.0:
            return
        magnitude = random.uniform(
            0.0, Group.CHAR_MUTATE_PARAM_1)/(Group.CHAR_MUTATE_PARAM_2
                + self.popl/Group.CHAR_MUTATE_PARAM_3)
        delta = magnitude/direction_norm*direction
        self.character += delta
        self.character = np.clip(
            self.character, Group.CHAR_MIN, Group.CHAR_MAX)

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

        self.mutate_character()

        self.consume_food()
        new_group = self.emigrate()
        self.decrease_popl()
        self.produce_food()

        self.perish()

        return new_group
