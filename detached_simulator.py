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

    TODO: Add run info file.

"""


from simulator import Simulation
import numpy as np


def run(sim, total_iter, out_file_path, log_iter=0):
    for it in range(total_iter):
        sim.next_step()
        if log_iter != 0 and it % log_iter == 0:
            print(it)
            pass  # log
    sim.save_object(out_file_path)


if __name__ == "__main__":
    pass
    # RANGE = (200, 2000)
    # TRIALS = 5
    # TEMP_COUNT = 10
    # ITER_COUNT = 10**3

    sim = Simulation(n_particles=1000, mass=1.2e-20, rad=0.01, T=237, dt=0.01, V=1)
    run(sim, 10**4, "data.pkl", 10**3)

    # temps = np.linspace(RANGE[0], RANGE[1], TEMP_COUNT)
    # for _ in range(TRIALS):
    #     # implement proper save
    #     for i, T in enumerate(temps):
    #         run(sim, total_iter=ITER_COUNT)
    #     sim.save_object()
