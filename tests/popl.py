import random

import matplotlib.pyplot as plt

from src.civ.tribe import Tribe
from src.field.cell import Cell


if __name__ == "__main__":
    # Players
    cell = Cell(0, 0)
    cell.stpn = 0.0007
    cell.surface = Cell.SURFACE_LAND

    tribe = Tribe(10, 20, cell)

    # Simulation
    sim_seed = 1
    random.seed(sim_seed)

    xs = []
    popls = []
    foods = []
    diffs = []

    for i in range(100):
        tribe.update()

        xs.append(i)
        popls.append(tribe.popl)
        foods.append(tribe.food)
        diffs.append(tribe.diff)

        if not tribe.alive:
            break

    # Graph
    fig, ax = plt.subplots(2, 1)
    ax_pf = ax[0]
    ax_d = ax[1]

    ax_pf.plot(xs, popls, label="Popl.")
    ax_pf.plot(xs, foods, label="Food")
    ax_pf.legend()
    ax_pf.set_xlabel("Turn")
    ax_pf.set_ylabel("Value")

    ax_d.plot(xs, diffs)
    ax_pf.set_xlabel("Turn")
    ax_d.set_ylabel("Difficulty")

    plt.show()
