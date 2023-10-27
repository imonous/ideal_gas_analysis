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


def run(sim, total_iter, out_file_path):
    """
    sim: the simulation object
    total_iter: total number of iterations
    out_file_path: the output file path (more convienient to accept string)
    [log_file]: log file (more convienient to accept file object)
    [log_iter]: how often to log (percentage)
    """
    for i in range(total_iter):
        sim.next_step()
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
            run(sim, ITER_COUNT, file_path)

    # sim = Simulation(n_particles=1000, mass=1.2e-20, rad=0.01, T=237, dt=0.01, V=1)
    # run(sim, total_iter=ITER_COUNT,
