"""

    This script executes the simulator with no GUI attached, returning only the
    results (particle velocities). 

    Script variables:
        SLIPE_EVERY_ITER : time to sleep every iteration in seconds
        BACKUP_ITER      : backup every BACKUP_ITER iterations
        OUT_FILE_PATH    : result file path
        TIME_TO_RUN      : total time in seconds to run the simulation
        VERBOSE          : whether to log the time passed and notify backups

    Simulation variables (see simulator.py): NUM_PARTICLES, PARTICLE_m,
    PARTICLE_r, GAS_T, GAS_V, SIM_dt.

    Using this script makes it realistic to run the simulation much faster than 
    real-time, given sufficient computing resources. Otherwise, a larger time 
    step would be required, which would result in less accuracy.

"""


from simulator import optimal_volume, Simulation
from time import sleep

from simulator import Simulation
from time import sleep


def run(sim, sleep_every_iter, backup_iter, total_iter, verbose):
    for it in range(total_iter):
        sim.next_step()
        if verbose:
            print(f"it {it} => {iter * SIM_dt}s...")
        if backup_iter % it == 0:
            print(f"Data backed up...")
        iter += 1
        sleep(sleep_every_iter)


if __name__ == "__main__":
    SLEEP_EVERY_ITER = 0
    BACKUP_ITER = 10**2
    # OUT_FILE_PATH = ""
    TOTAL_ITER = 10**5
    VERBOSE = False

    NUM_PARTICLES = 1000
    PARTICLE_m = 1.2e-20
    PARTICLE_r = 0.01
    GAS_T = 237
    GAS_V = optimal_volume(PARTICLE_r, NUM_PARTICLES)
    SIM_dt = 0.01

    sim = Simulation(NUM_PARTICLES, PARTICLE_m, PARTICLE_r, GAS_T, GAS_V, SIM_dt)
    # out_file = open(OUT_FILE_PATH)

    run(sim, SLEEP_EVERY_ITER, BACKUP_ITER, TOTAL_ITER, VERBOSE)
