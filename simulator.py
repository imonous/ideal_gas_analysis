""" 
BASED ON: https://github.com/labay11/ideal-gas-simulation 

Memory usage: linear => N/10 MiB, where N is the number of particles
CPU heavy
"""


import numpy as np

k_B = 1.380648e-23  # boltzmann contant (J/K)


def mod(v):
    """computes the squared sum over the last axis of the numpy.ndarray v"""
    return np.sum(v * v, axis=-1)


def pmod(v, T, m):
    """
    Maxwell-Boltzmann's distribuion of probability
    for the length of the velocity vector v at temprature T
    for a particle of mass m
    """
    return (
        4
        * np.pi
        * v**2
        * np.power(m / (2 * np.pi * k_B * T), 3 / 2)
        * np.exp(-m * v**2 / (2 * k_B * T))
    )


class Simulation:
    def __init__(self, n_particles, mass, rad, T, V, dt=0.2):
        self.PART = n_particles  # PARTICLE NUMBER
        self.MASS = mass
        self.RAD = rad  # PARTICLE RADIUS
        self.DIAM = 2 * rad  # PARTICLE DIAMETER

        self.T = T  # SYSTEM TEMPERATURE
        self.V = V

        self.L = np.power(self.V, 1 / 3)  # SIDE LENGTH
        self.halfL = self.L / 2  # HALF SIDE LENGTH

        self.dt = dt  # TIME DIFFERENCE EACH STEP
        self.dv = 0.2  # DIFFERENCE IN VELOCITY EACH STEP

        self.init_particles()  # INIT PARTICLE POSITIONS AND VELOCITIES

    def _update_velocities(self):
        v_polar = np.random.random((self.PART, 2))  # RANDOM VELOCITIES PARTx2

        self.v = np.zeros((self.PART, 3))

        self.v[:, 0] = np.sin(v_polar[:, 0] * np.pi) * np.cos(v_polar[:, 1] * 2 * np.pi)
        self.v[:, 1] = np.sin(v_polar[:, 0] * np.pi) * np.sin(v_polar[:, 1] * 2 * np.pi)
        self.v[:, 2] = np.cos(v_polar[:, 0] * np.pi)

        vrms = np.sqrt(3 * k_B * self.T / self.MASS)  # RMS VELOCITY
        self.v *= vrms

    def init_particles(self):
        """
        Init the particles positions and velocities.

        The initial positions are completely random inside the box.

        The initial velocities are generated by a random unitary vector with
        a length given by the average velocity (vmed) at the system temperature.
        """
        self.r = np.random.rand(self.PART, 3) * 2 * (self.halfL - self.RAD) - (
            self.halfL - self.RAD
        )  # POSITION
        self._update_velocities()

    def set_temperature(self, T):
        self.T = T
        self._update_velocities()

    def next_step(self):
        """calculate the next step"""
        # update the position
        self.r += self.dt * self.v

        # check for collitions with other particles
        dists = np.sqrt(mod(self.r - self.r[:, np.newaxis]))
        cols2 = (0 < dists) & (dists < self.DIAM)
        idx_i, idx_j = np.nonzero(cols2)
        for i, j in zip(idx_i, idx_j):
            if j < i:
                # skip duplications and same particle
                continue

            rij = self.r[i] - self.r[j]
            d = mod(rij)
            vij = self.v[i] - self.v[j]
            dv = np.dot(vij, rij) * rij / d
            self.v[i] -= dv
            self.v[j] += dv

            # update the positions so they are no longer in contact
            self.r[i] += self.dt * self.v[i]
            self.r[j] += self.dt * self.v[j]

        # check for collition with the walls
        walls = np.nonzero(np.abs(self.r) + self.RAD > self.halfL)
        self.v[walls] *= -1
        self.r[walls] -= self.RAD * np.sign(self.r[walls])

    def get_points(self):
        return (self.r[:, 0], self.r[:, 1], self.r[:, 2])


# sim = Simulation(500, 1.2e-20, 0.01, 500, 2, 0.05)
