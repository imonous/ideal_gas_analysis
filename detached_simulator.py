"""

    This script executes the simulator with no GUI attached, returning only the
    results (particle velocities). 

    Script variables:
        SLIPE_EVERY_ITER : time to sleep every iteration in seconds
        BACKUP_ITER      : backup every BACKUP_ITER iterations
        TIME_TO_RUN      : total time in seconds to run the simulation
        VERBOSE          : whether to log the time passed and notify backups

    Simulation variables (see simulator.py): NUM_PARTICLES, PARTICLE_m,
    PARTICLE_r, GAS_T, GAS_V, SIM_dt.

    Using this script makes it realistic to run the simulation much faster than 
    real-time, given sufficient computing resources. Otherwise, a larger time 
    step would be required, which would result in less accuracy.

    Data is backed up to "./out.csv".

"""


import numpy as np
from simulator import Simulation
from time import sleep


OUT_FILE_PATH = "./out.csv"


def save_np_arr(arr, out_file_path=OUT_FILE_PATH):
    np.savetxt(out_file_path, arr, delimiter=",")


def load_np_arr(out_file_path=OUT_FILE_PATH):
    return np.genfromtxt(out_file_path, delimiter=",")


def run(sim, sleep_every_iter, backup_iter, total_iter, verbose):
    times_backed = 1
    for it in range(total_iter):
        sim.next_step()
        if verbose:
            print(f"{it}/{total_iter}")
        if it == backup_iter * times_backed:
            save_np_arr(sim.get_velocities())
            times_backed += 1
            if verbose:
                print(f"Data backed up...")
        it += 1
        sleep(sleep_every_iter)
    save_np_arr(sim.r)


if __name__ == "__main__":
    sim = Simulation(
        n_particles=1000,
        mass=1.2e-20,
        rad=0.01,
        T=237,
        V=None,
        dt=0.01,
    )
    run(
        sim=sim,
        sleep_every_iter=0,
        backup_iter=10**2,
        total_iter=10**5,
        verbose=True,
    )
