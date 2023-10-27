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


from simulation import Simulation
import numpy as np


def run(sim, total_iter, out_file_path, log_file=None, log_iter=0):
    """
    sim: the simulation object
    total_iter: total number of iterations
    out_file_path: the output file path (append mode) (more convienient to accept string)
    [log_iter]: how often to log (percentage as decimal)
    [log_file]: log file (more convienient to accept file object)
    """
    n = int(log_iter * total_iter)
    for i in range(total_iter):
        sim.next_step()
        if n != 0 and i % n == 0:
            progress = round(log_iter * (i // n), 2)
            log_file.write(f"{out_file_path}: {progress * 100}%\n")
        elif n != 0 and i == total_iter - 1:
            log_file.write(f"{out_file_path}: DONE!\n")
    sim.save_object(out_file_path)


# The experiment
if __name__ == "__main__":
    # Experiment constants
    RANGE = (200, 2000)
    TRIALS = 2  # 5
    TEMP_COUNT = 2  # 10
    ITER_COUNT = 10  # 10**4

    # Simulation constants
    PARTICLE_COUNT = 1000
    PARTICLE_MASS = 1.2e-20
    PARTICLE_RADIUS = 0.01
    GAS_VOLUME = 1
    TIME_STEP = 0.01

    with open("./data/log.txt", "w"):  # clear log contents
        pass
    log_file = open("./data/log.txt", "a")
    for temp in np.linspace(*RANGE, TEMP_COUNT):
        for trial in range(1, TRIALS + 1):
            file_path = f"./data/temp{int(temp)}trial{trial}.pkl"
            sim = Simulation(
                n_particles=PARTICLE_COUNT,
                mass=PARTICLE_MASS,
                rad=PARTICLE_RADIUS,
                T=temp,
                dt=TIME_STEP,
                V=GAS_VOLUME,
            )
            run(sim, ITER_COUNT, file_path, log_file, log_iter=0.2)
    log_file.close()
