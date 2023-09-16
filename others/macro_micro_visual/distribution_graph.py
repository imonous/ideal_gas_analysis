# Due to an unexpected result from the 2nd graph ("Probability difference").

from math import comb

import matplotlib as mpl
import matplotlib.pyplot as plt

import seaborn as sns
import gi


def scale(L, k):
    # There is a way more efficient way to do this, but im tired bye
    return [round(n * k) for n in L]


if __name__ == "__main__":
    # Default theme
    gi.require_version("Gtk", "3.0")
    mpl.use("module://mplcairo.gtk")
    sns.set_theme()

    # Data
    COLUMNS, ROWS = 2, 4
    MAX_N = 1031  # max before error

    # Create grid
    fig, axes = plt.subplots(COLUMNS, ROWS)

    # Subplots
    max_n = MAX_N // (COLUMNS * ROWS)
    for p in range(COLUMNS * ROWS):
        x, y = [], []
        for n in range(0, max_n + 1):
            x.append(n)
            y.append(comb(max_n, n))
        k = 100 / max(x)
        x, y = scale(x, k), scale(y, k)

        ax_y, ax_x = p // ROWS, p % ROWS
        sns.lineplot(x=x, y=y, ax=axes[ax_y, ax_x])
        axes[ax_y, ax_x].set_title(f"Plot {p}")

        max_n += MAX_N // (COLUMNS * ROWS)

    # Adjust and display
    plt.tight_layout()
    plt.show()
