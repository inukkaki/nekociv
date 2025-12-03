import random

import matplotlib.pyplot as plt

from src.civ.group import Group
from src.field.cell import Cell

N_TURN = 1000


if __name__ == "__main__":
    # Players
    c1 = Cell(0, 0)
    c1.stpn = 0.0007
    c1.surface = Cell.SURFACE_LAND

    c2 = Cell(0, 1)
    c2.stpn = 0.0005
    c2.surface = Cell.SURFACE_LAND

    c3 = Cell(1, 0)
    c3.stpn = 0.0001
    c3.surface = Cell.SURFACE_LAND

    c1.neighborhood = [c2, c3]
    c2.neighborhood = [c3, c1]
    c3.neighborhood = [c1, c2]

    Group(10, 20, [0.5, 0.5, 0.5], c1)
    Group(10, 20, [0.5, 0.5, 0.5], c2)
    Group(10, 20, [0.5, 0.5, 0.5], c3)

    # Simulation
    sim_seed = 1
    random.seed(sim_seed)
    c1.init_rng(random.randint(1, 2**31 - 1))
    c2.init_rng(random.randint(1, 2**31 - 1))
    c3.init_rng(random.randint(1, 2**31 - 1))

    xs = []
    popls = []
    foods = []
    diffs = []

    for i in range(N_TURN):
        if c1.group != None and c1.group.alive:
            c1.group.update()
        if c2.group != None and c2.group.alive:
            c2.group.update()
        if c3.group != None and c3.group.alive:
            c3.group.update()

        xs.append(i)
        if c1.group != None:
            popls.append(c1.group.popl)
            foods.append(c1.group.food)
            diffs.append(c1.group.diff)
        else:
            popls.append(0)
            foods.append(0)
            diffs.append(0.0)

    # Graph
    fig, ax = plt.subplots(2, 1)
    ax_pf = ax[0]
    ax_d = ax[1]

    ax_pf.plot(xs, popls, label="Popl.", alpha=0.5)
    ax_pf.plot(xs, foods, label="Food", alpha=0.5)
    ax_pf.legend()
    ax_pf.set_ylabel("Value")

    ax_d.plot(xs, diffs)
    ax_d.set_xlabel("Turn")
    ax_d.set_ylabel("Difficulty")

    plt.show()
