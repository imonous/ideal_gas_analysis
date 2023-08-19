import mbd

from molmass import Formula
import numpy as np

import matplotlib as mpl
import gi


def diagram1(mbdg):
    mbdg.mbd_kinetic(temps=[273], E_act=1.5e-20, shade=True, verbose=True).set_view(
        title="Maxwell-Boltzmann distribution for Helium at 273K",
        legend=False,
        ticks=False,
    ).save(filename="diagrams/diagram1")


if __name__ == "__main__":
    gi.require_version("Gtk", "3.0")
    mpl.use("module://mplcairo.gtk")

    compound = Formula("He")
    mbdg = mbd.MBDGraphs(compound)
