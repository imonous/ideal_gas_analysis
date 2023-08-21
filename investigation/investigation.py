import mbd

from molmass import Formula
import numpy as np

import matplotlib as mpl
import gi


def data_process(mbdg):
    mbdg.mbd_succ_coll_kinetic(
        E_acts=np.linspace(0.7e-19, 3e-19, 10)[:5:],
        E_act_labels=np.linspace(20e3, 400e3, 10)[:5],
    ).set_view().save("diagrams/raw_data1")

    mbdg.clear()

    mbdg.mbd_succ_coll_kinetic(
        E_acts=np.linspace(0.7e-19, 3e-19, 10)[5:],
        E_act_labels=np.linspace(20e3, 400e3, 10)[5:],
    ).set_view().save("diagrams/raw_data2")


def analysis(mbdg):
    mbdg.mbd_succ_coll_kinetic(
        E_acts=[1.5e-19], E_act_labels=[200e3], base_f=mbd.base_log, verbose=True
    ).set_view().save("diagrams/processed_data_fit")


def arrhenius(mbdg):
    mbdg.mbd_succ_coll_kinetic(
        E_acts=[1.5e-19], E_act_labels=[200e3], base_f=mbd.base_arrhenius, verbose=True
    ).set_view().save("diagrams/processed_data_fit")


if __name__ == "__main__":
    gi.require_version("Gtk", "3.0")
    mpl.use("module://mplcairo.gtk")

    compound = Formula("He")
    mbdg = mbd.MBDGraphs(compound)

    arrhenius(mbdg)
