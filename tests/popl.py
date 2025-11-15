import random

import matplotlib.pyplot as plt

from src.civ.group import Group
from src.field.cell import Cell

N_TURN = 3000


if __name__ == "__main__":
    # Players
    cell = Cell(0, 0)
    cell.stpn = 0.0007
    cell.surface = Cell.SURFACE_LAND

    group = Group(10, 20, cell)

    # Simulation
    sim_seed = 1
    random.seed(sim_seed)

    xs = []
    popls = []
    foods = []
    diffs = []

    for i in range(N_TURN):
        group.update()

        xs.append(i)
        popls.append(group.popl)
        foods.append(group.food)
        diffs.append(group.diff)

        if not group.alive:
            break

    # Graph
    fig, ax = plt.subplots(2, 1)
    ax_pf = ax[0]
    ax_d = ax[1]

    ax_pf.plot(xs, popls, label="Popl.")
    ax_pf.plot(xs, foods, label="Food")
    ax_pf.legend()
    ax_pf.set_ylabel("Value")

    ax_d.plot(xs, diffs)
    ax_d.set_xlabel("Turn")
    ax_d.set_ylabel("Difficulty")

    plt.show()
