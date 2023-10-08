"""

    This script executes the simulator with no GUI attached, returning only the
    results (particle velocities). 

    Script variables:
        SLIPE_EVERY_ITER : time to sleep every iteration in seconds
        BACKUP_ITER  : backup every BACKUP_ITER iterations
        OUT_FILE_PATH: result file path
        TIME_TO_RUN  : total time in seconds to run the simulation
        VERBOSE      : whether to log the time passed and notify backups

    Simulation variables (see simulator.py): NUM_PARTICLES, PARTICLE_m,
    PARTICLE_r, GAS_T, GAS_V, SIM_dt.

    Using this script makes it realistic to run the simulation much faster than 
    real-time, given sufficient computing resources. Otherwise, a larger time 
    step would be required, which would result in less accuracy.

"""


from simulator import Simulation
from time import sleep

SLEEP_EVERY_ITER = 0
BACKUP_ITER = 10**2
# OUT_FILE_PATH = ""
TIME_TO_RUN = 60 * 1
VERBOSE = False

NUM_PARTICLES = 1000
PARTICLE_m = 1.2e-20
PARTICLE_r = 0.01
GAS_T = 237
GAS_V = 2
SIM_dt = 0.01

sim = Simulation(NUM_PARTICLES, PARTICLE_m, PARTICLE_r, GAS_T, GAS_V, SIM_dt)
# out_file = open(OUT_FILE_PATH)

iter = 0
while True:
    sim.next_step()
    # if iter % BACKUP_ITER == 0:
    #     out_file.write(sim.r)
    print(f"Running for {iter * SIM_dt}s...")
    iter += 1
    if iter * SIM_dt >= TIME_TO_RUN:
        break
    sleep(SLEEP_EVERY_ITER)
