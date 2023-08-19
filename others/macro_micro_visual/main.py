# Macro states are composed of many micro states. Each micro state has a
# probability (usually identical). It is said that a system made up of many 
# possible micro states will settle on the one with most micro states.

# A real world example: coin flip. For n coins, the number of possible
# configurations (micro states) is 2^n. The number of possible heads vs tails
# (macro states) is n+1. All micro states are equally probable. The most 
# probable macro state is n/2 heads and n/2 tails, because it has most micro
# states (n choose n/2).

# Context: aforemetioned coin flip. With respect to n, graph difference between 
# probability of [most probable macro state] and [2nd most probable macro 
# state]. Given the initial theorem, the graph should increase exponentially.


from math import comb

import matplotlib.pyplot as plt
import matplotlib as mpl

import seaborn as sns
import gi



class Difference:
    def __init__(self, n):
        if n % 2 != 0:
            raise Exception("n must be even") # to simplify
        self.n = n
        self.max_micro = comb(n, n//2) # most probable
        self.max2_micro = comb(n, n//2 - 1) # second most probable
        self.total_micro = 2**n

    def absolute_difference(self):
        return self.max_micro - self.max2_micro

    def max_probability(self):
        p = self.max_micro / self.total_micro
        return round(p * 100, 2)


if __name__ == "__main__":
    gi.require_version("Gtk", "3.0")
    mpl.use("module://mplcairo.gtk")
    sns.set_theme()


    # Data
    MAX_N = 1000
    x, y1, y2 = [], [], []
    for n in range(2, MAX_N, 2):
        diff = Difference(n)
        x.append(n)
        y1.append(diff.absolute_difference())
        y2.append(diff.max_probability())

    # Create grid
    fig, axes = plt.subplots(1, 2)

    # First subplot
    sns.lineplot(x=x, y=y1, ax=axes[0])
    axes[0].set_title("Absolute difference")

    # Second subplot
    sns.lineplot(x=x, y=y2, ax=axes[1])
    axes[1].set_title("Maximum probability")

    # Adjust and display
    plt.tight_layout()
    plt.show()

    
