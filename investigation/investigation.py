import mbd

from molmass import Formula
import numpy as np

import matplotlib as mpl
import gi

from py_markdown_table.markdown_table import markdown_table


PATH = "/home/anon/Programming/projects/ideal_gas_analysis/investigation"


def data_process(mbdg):
    mbdg.mbd_succ_coll_kinetic(
        E_acts=np.linspace(0.7e-19, 3e-19, 10)[:5:],
        E_act_labels=np.linspace(20e3, 400e3, 10)[:5],
    ).set_view().save(f"{PATH}/diagrams/raw_data1")

    mbdg.clear()

    mbdg.mbd_succ_coll_kinetic(
        E_acts=np.linspace(0.7e-19, 3e-19, 10)[5:],
        E_act_labels=np.linspace(20e3, 400e3, 10)[5:],
    ).set_view().save(f"{PATH}/diagrams/raw_data2")


def save_raw_data_md(mbdg):
    pass


def analysis(mbdg):
    mbdg.mbd_succ_coll_kinetic(
        E_acts=[1.5e-19], E_act_labels=[200e3], base_f=mbd.base_log, verbose=True
    ).set_view().save(f"{PATH}/diagrams/processed_data_fit")


def arrhenius(mbdg):
    mbdg.mbd_succ_coll_kinetic(
        E_acts=[1.5e-19], E_act_labels=[200e3], base_f=mbd.base_arrhenius, verbose=True
    ).set_view().save(f"{PATH}/diagrams/processed_data_fit")


if __name__ == "__main__":
    gi.require_version("Gtk", "3.0")
    mpl.use("module://mplcairo.gtk")

    compound = Formula("He")
    mbdg = mbd.MBDGraphs(compound)

    data = []
    tick = 0
    for entry in mbdg.generate_raw(
        temps=np.linspace(200, 20000, 25)
    ):  # github size limit
        T, E, P = entry
        for i in range(len(E)):
            data.append(
                {
                    "Temperature, K": round(T, 4),
                    "Kinetic energy, kJ": round(E[i] * 1e20, 4),
                    "Probability": round(P[i], 4),
                }
            )
        print(tick)
        tick += 1
    with open(f"{PATH}/raw_data.md", "w") as file:
        markdown = markdown_table(data).get_markdown()
        file.write(markdown)
