"""

    This script executes the simulator with no GUI attached, returning only the
    results (particle velocities). 

    Script variables:
        VERBOSE : whether to log the time passed and notify backups
        ...

    Simulation variables: (see simulator.py)

    Using this script makes it realistic to run the simulation much faster than 
    real-time, given sufficient computing resources. Otherwise, a larger time 
    step would be required, which would result in less accuracy.

    Data is backed up to "./data.pkl" by default.

"""


import numpy as np
from simulator import Simulation


def run(sim, total_iter, verbose=True, backup_iter=0, out_file_path="data.pkl"):
    try:
        times_backed = 0
        for it in range(total_iter):
            sim.next_step()
            if verbose:
                print(f"{it}/{total_iter}")
            it += 1
            if it == backup_iter * (times_backed + 1):
                sim.save_object(out_file_path)
                times_backed += 1
                print(f"Data backed up...")
        sim.save_object(out_file_path)
    except KeyboardInterrupt:
        sim.save_object(out_file_path)


if __name__ == "__main__":
    # temps = np.linspace(0, 2000, 3)
    # fake_mbd = np.array([])
    # for T in temps:
    sim = Simulation(
        n_particles=1000,
        mass=1.2e-20,
        rad=0.01,
        T=237,
        dt=0.01,
    )
    run(sim, total_iter=500)
    #     parts_above_vrms = sim.get_velocities() > sim.vrms
    #     np.append(fake_mbd, parts_above_vrms)
    # print(temps, fake_mbd)
