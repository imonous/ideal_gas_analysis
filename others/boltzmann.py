# Refer to "Concepts in Thermal Physics" by Blundell, example 4.2


from random import randint

import numpy as np

import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.animation as animation

import gi


gi.require_version("Gtk", "3.0")
mpl.use("module://mplcairo.gtk")

SIDE_LENGTH = 20
INIT_VALUE = 1
BARS = 6
START_FRAME = 10**0

system = np.full((SIDE_LENGTH, SIDE_LENGTH), INIT_VALUE, dtype=int)

fig = plt.figure()
axes = fig.add_subplot(1, 1, 1)
plt.xticks(np.arange(0, BARS, 1.0))
axes.set_ylim(0, 400)

x, heights = np.arange(BARS), np.zeros(BARS, dtype=int)
bars = plt.bar(x, heights, width=1.0, facecolor="grey", edgecolor="white")


def distribution(system):
    return [np.count_nonzero(system == i) for i in range(BARS)]


def increment_system(system):
    x_old, y_old, x_new, y_new = (randint(0, SIDE_LENGTH - 1) for _ in range(4))
    if system[y_old][x_old] > 0:
        system[y_new][x_new] += 1
        system[y_old][x_old] -= 1


def animate(i):
    increment_system(system)
    heights = distribution(system)
    for j, bar in enumerate(bars):
        print(i)
        bar.set_height(heights[j])
    return bars


if __name__ == "__main__":
    for _ in range(START_FRAME):
        increment_system(system)

    anim = animation.FuncAnimation(
        fig, animate, repeat=False, interval=1, frames=10000, blit=True
    )
    plt.show()


# TODO:
# 1) Define equilibrium ?= when functions match?
# 2) Define the ideal function
# 3) Portray when functions match
