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
import multiprocessing
from functools import partial
from simulation import Simulation


def run(sim, out_file_path, total_iter, log_file_path=None, log_iter=0):
    """
    sim: the simulation object
    out_file_path: the output file path (append mode) (more convienient to accept string)
    total_iter: total number of iterations
    [log_iter]: how often to log (percentage as decimal)
    [log_file]: log file (more convienient to accept file object)
    """
    if log_iter:
        log_file = open(log_file_path, "a")
    n = int(log_iter * total_iter)
    for i in range(total_iter):
        sim.next_step()
        if log_iter and i % n == 0:
            progress = round(log_iter * (i // n), 2)
            log_file.write(f"{out_file_path}: {progress * 100}%\n")
            log_file.flush()
        elif log_iter and i == total_iter - 1:
            log_file.write(f"{out_file_path}: DONE!\n")
            log_file.flush()
    if log_iter:
        log_file.close()
    sim.save_object(out_file_path)


# The experiment
if __name__ == "__main__":
    # Experiment constants
    RANGE = (200, 2000)
    TRIALS = 2  # 5
    TEMP_COUNT = 2  # 10
    ITER_COUNT = 10**3  # 10**4

    # Simulation constants
    PARTICLE_COUNT = 1000
    PARTICLE_MASS = 1.2e-20
    PARTICLE_RADIUS = 0.01
    GAS_VOLUME = 1
    TIME_STEP = 0.01

    args = []
    for temp in np.linspace(*RANGE, TEMP_COUNT):
        for trial in range(1, TRIALS + 1):
            sim = Simulation(
                n_particles=PARTICLE_COUNT,
                mass=PARTICLE_MASS,
                rad=PARTICLE_RADIUS,
                T=temp,
                dt=TIME_STEP,
                V=GAS_VOLUME,
            )
            file_path = f"./data/temp{int(temp)}trial{trial}.pkl"
            args.append((sim, file_path))

    log_file_path = "./data/log.txt"
    with open(log_file_path, "w"):  # clear log contents
        pass
    func = partial(
        run, total_iter=ITER_COUNT, log_file_path=log_file_path, log_iter=0.2
    )
    with multiprocessing.Pool(processes=2) as pool:
        pool.starmap(func, args)
        pool.close()
        pool.join()
