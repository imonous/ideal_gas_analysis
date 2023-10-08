"""
    This script executes the simulator with no GUI attached, returning only the
    results (particle velocities). 

    Script variables:
        RATE_LIMITER : how many iterations per second
        BACKUP_IT    : backup every BACKUP_ITER iterations
        OUT_FILE_NAME: result file name
        TIME_TO_RUN  : total time in seconds to run the simulation
        VERBOSE      : whether to log the time passed and notify backups

    Simulation variables (see simulator.py): NUM_PARTICLES, PARTICLE_m,
    PARTICLE_r, GAS_T, GAS_V, SIM_dt.

    Using this script makes it realistic to run the simulation much faster than 
    real-time, given sufficient computing resources. Otherwise, a larger time 
    step would be required, which would result in less accuracy.
"""
