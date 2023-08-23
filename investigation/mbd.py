import matplotlib as mpl
import matplotlib.pyplot as plt

import numpy as np

from scipy.constants import pi, Boltzmann as k_B, Avogadro as N_A, R
from scipy.integrate import simpson
from scipy.optimize import curve_fit

from math import e, sqrt


def mbd(v, m, T):
    """The Maxwell-Boltzmann distribution."""
    beta = 1 / (k_B * T)  # common shorthand
    nf = 4 / pi**0.5 * (0.5 * m * beta) ** 1.5  # normalization factor
    return nf * v**2 * e ** (-0.5 * m * v**2 * beta)


def base_log(x, a, b):
    """The logarithmic function."""
    return a * np.log(x) + b


# TODO: define properly
def base_arrhenius(T, A, k):
    """The arrhenius equation."""
    return A * e ** (-k / T)


# TODO: figure out graphing a saving better
# TODO: improve naming
# TODO: add docs
# TODO: adjust linspace more intelligently
# TODO: improve visuals
class MBDGraphs:
    def __init__(self, compound, root_dir="./investigation"):
        self.pmass = compound.mass * 1e-3 / N_A  # particle mass
        self.root_dir = root_dir
        plt.figure()

    # TODO: adjust x upper inteligently
    def mbd(
        self, temps=np.linspace(100, 4000, 4), v_act=None, shade=False, verbose=False
    ):
        """The Maxwell-Boltzmann distribution with respect to velocity."""
        if shade and v_act is None:
            raise ValueError("If shade is True, v_act must be provided.")
        if shade and len(temps) != 1:
            raise ValueError("If shade is True, the length of temps must be 1.")

        x = np.linspace(0, 10000, 10000)
        for T in temps:
            y = mbd(x, self.pmass, T)
            plt.plot(x, y, label=f"T={round(T)}K")

            if verbose:
                area = simpson(y, x)
                print(f"Area is {area: .2f} for {round(T)}K")

        if v_act:
            plt.vlines(
                x=v_act,
                ymin=0,
                ymax=mbd(v_act, self.pmass, T),
                colors=["black"],
                linestyles="dashed",
                label=f"v_act={v_act}m/s",
            )

        if shade:
            plt.fill_between(x, y, where=(x >= v_act), alpha=0.2)

        plt.xlabel("Speed (v, m/s)")
        plt.ylabel("Probability (P)")

        return self

    def mbd_kinetic(
        self, temps=np.linspace(1000, 4000, 4), E_act=None, shade=False, verbose=False
    ):
        """The Maxwell-Boltzmann distribution with respect to kinetic energy."""
        if shade and E_act is None:
            raise ValueError("If shade is True, E_act must be provided.")
        if shade and len(temps) != 1:
            raise ValueError("If shade is True, the length of temps must be 1.")

        x_v = np.linspace(0, 20000, 30000)  # velocity
        x_E = np.vectorize(lambda v: 0.5 * self.pmass * v**2)(x_v)  # energy
        nf = 1  # normalisation factor

        print(len(temps))
        for T in temps:
            y = mbd(x_v, self.pmass, T)
            nf = 1 / simpson(y, x_E)
            y *= nf  # normalise
            plt.plot(x_E, y, label=f"T={round(T)}K")

            if verbose:
                area = simpson(y, x_E)
                print(f"Area is {area: .2f} for {round(T)}K")

        if E_act:
            v_act = sqrt(2 * E_act / self.pmass)
            plt.vlines(
                x=E_act,
                ymin=0,
                ymax=mbd(v_act, self.pmass, T) * nf,
                colors=["black"],
                linestyles="dashed",
                label=f"E_act={E_act}J",
            )

        if shade:
            plt.fill_between(x_E, y, where=(x_E >= E_act), alpha=0.2)

        plt.xlabel(r"Kinetic energy (E$_k$, J)")
        plt.ylabel("Probability (P)")

        return self

    # TODO: set up init view
    def mbd_3d(self, low_temp=100, up_temp=4000):
        """TODO"""
        X = np.linspace(low_temp, up_temp, 200)  # temp
        Y = np.linspace(0, 15000, 200)  # speed
        Z = np.array([mbd(Y, self.pmass, T) for T in X])
        Y, X = np.meshgrid(X, Y)

        ax = plt.axes(projection="3d")
        ax.plot_surface(X, Y, Z, cmap="viridis", edgecolor="none")

        ax.set_xlabel("Temperature")
        ax.set_ylabel("Speed")
        ax.set_zlabel("Probability")
        ax.set_title("The Maxwell-Boltzmann distribution in 3d")

        return self

    def mbd_succ_coll(
        self, low_v_act=1000, up_v_act=10000, fit_curve=False, base_f=None
    ):
        """TODO"""
        if fit_curve and base_f is None:
            raise ValueError("If fit is True, base_f must be provided.")

        vel = np.linspace(0, 50000, 30000)
        for v_act in np.linspace(low_v_act, up_v_act, 4):
            index = np.where(vel > v_act)[0][0]
            x, y = np.array([]), np.array([])
            for T in np.linspace(1000, 20000, 1000):
                prob = mbd(vel, self.pmass, T)
                area = simpson(prob[index:], vel[index:])
                x = np.append(x, T)
                y = np.append(y, area)
            plt.plot(x, y, label=f"v_act={round(v_act)}m/s")

            if fit_curve:
                parameters, covariance = curve_fit(base_f, x, y)
                SE = np.sqrt(np.diag(covariance))
                fit = base_f(x, *parameters)
                plt.plot(x, fit, "--", label=f"curve_fit for {round(v_act)}")
                print(f"v_act={round(v_act)}K\nparams: {parameters}\nstd err: {SE}\n")

        plt.xlabel("Temperature")
        plt.ylabel("Area")

        return self

    def mbd_succ_coll_kinetic(
        self,
        E_acts=np.linspace(0.7e-19, 3e-19, 4),
        E_act_labels=None,
        temps=np.linspace(200, 20000, 5000),
        base_f=None,
        verbose=False,
    ):
        """TODO"""
        x_v = np.linspace(0, 50000, 30000)
        x_E = np.vectorize(lambda v: 0.5 * self.pmass * v**2)(x_v)  # energy
        for iter, E_act in enumerate(E_acts):
            index = np.where(x_E > E_act)[0][0]
            x_T, y_area = np.array([]), np.array([])
            for T in temps:
                y_prob = mbd(x_v, self.pmass, T)
                y_prob *= 1 / simpson(y_prob, x_E)  # normalise
                area = simpson(y_prob[index:], x_E[index:])
                x_T = np.append(x_T, T)
                y_area = np.append(y_area, area)
            label = (
                f"E_act={round(E_act if E_act_labels is None else E_act_labels[iter])}J"
            )
            plt.plot(x_T, y_area, label=label)

            if base_f:
                params, covariance = curve_fit(base_f, x_T, y_area)
                label = f"curve_fit for {round(E_act if E_act_labels is None else E_act_labels[iter])}J"
                plt.plot(x_T, base_f(x_T, *params), "--", label=label)
                if verbose:
                    SE = np.sqrt(np.diag(covariance))
                    print(f"E_act={E_act}J\nparams: {params}\nstd err: {SE}\n")

        plt.xlabel("Temperature")
        plt.ylabel("Fraction of particles")

        plt.ylim(bottom=0, top=1)

        return self

    def generate_raw(
        self,
        E_acts=np.linspace(0.7e-19, 3e-19, 4),
        E_act_labels=None,
        temps=np.linspace(200, 20000, 5000),
    ):
        """TODO"""
        x_v = np.linspace(0, 50000, 30000)
        x_E = np.vectorize(lambda v: 0.5 * self.pmass * v**2)(x_v)  # energy
        for T in temps:
            y_prob = mbd(x_v, self.pmass, T)
            y_prob *= 1 / simpson(y_prob, x_E)  # normalise
            yield T, x_E, y_prob

    def set_view(self, title=None, legend=True, grid=True, ticks=True):
        """TODO"""
        if not ticks:
            plt.xticks([])
            plt.yticks([])
        plt.legend() if legend else None
        plt.grid(grid)
        plt.title(title)
        plt.tight_layout()
        plt.ticklabel_format(style="sci", axis="y", scilimits=(0, 0), useMathText=True)
        plt.ticklabel_format(style="sci", axis="x", scilimits=(0, 0), useMathText=True)

        return self

    def show(self):
        """TODO"""
        plt.show()

    def save(self, filename="result"):
        """TODO"""
        plt.savefig(f"{self.root_dir}/{filename}.png", dpi=300)

    def clear(self):
        plt.clf()
