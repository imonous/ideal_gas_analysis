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


def run(
    sim, total_iter, backup=True, backup_iter=0, verbose=True, out_file_path="data.pkl"
):
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
    if backup:
        sim.save_object(out_file_path)


if __name__ == "__main__":
    temps = np.linspace(273, 2000, 3)
    fake_mbd = np.array([])
    vrms = 0
    for i, T in enumerate(temps):
        sim = Simulation(n_particles=1000, mass=1.2e-20, rad=0.01, T=T, dt=0.01)
        run(sim, total_iter=500, backup=False)
        velocities = sim.get_velocities()
        if i == 0:
            vrms = np.average(velocities)
        parts_above_vrms = np.count_nonzero(velocities > vrms)
        fake_mbd = np.append(fake_mbd, parts_above_vrms)
    print(temps, fake_mbd)
