""" 

BASED ON: https://github.com/labay11/ideal-gas-simulation 

* Memory usage: linear => N/10 MiB, where N is the number of particles
* However, CPU heavy

"""


import numpy as np
import pickle

k_B = 1.380648e-23  # boltzmann contant (J/K)


def optimal_volume(r, N):
    """
    In order for collisions to happen on a "short" period of time so as to see how
    the velocities converge to the Maxwell-Boltzmann distribution, the radius of the
    particles must be ~(V/N)^(1/3). Otherwise, the momentum exchanged after each
    iteration will be small.

    Unusable for radius (roughly) <1.
    """
    return r**3 * N


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
    def __init__(self, n_particles, mass, rad, T, dt, V=None):
        self.PART = n_particles  # PARTICLE NUMBER
        self.MASS = mass
        self.RAD = rad  # PARTICLE RADIUS
        self.DIAM = 2 * rad  # PARTICLE DIAMETER

        self.T = T  # SYSTEM TEMPERATURE
        self.V = V
        if V is None:  # TODO: FIX! DOESNT WORK
            self.V = optimal_volume(self.RAD, self.PART)

        self.L = np.power(self.V, 1 / 3)  # SIDE LENGTH
        self.halfL = self.L / 2  # HALF SIDE LENGTH

        self.dt = dt  # TIME DIFFERENCE EACH STEP

        self.max_v = np.sqrt(2 * k_B * self.T / self.MASS)
        self.min_v = 0

        # histogram
        self.bin_width = 0.2
        self.bin_count = int((self.max_v * 3 - self.min_v) / self.bin_width)

        self.init_particles()  # INIT PARTICLE POSITIONS AND VELOCITIES

    def _update_velocities(self):
        v_polar = np.random.random((self.PART, 2))  # RANDOM VELOCITIES PARTx2

        self.v = np.zeros((self.PART, 3))

        self.v[:, 0] = np.sin(v_polar[:, 0] * np.pi) * np.cos(v_polar[:, 1] * 2 * np.pi)
        self.v[:, 1] = np.sin(v_polar[:, 0] * np.pi) * np.sin(v_polar[:, 1] * 2 * np.pi)
        self.v[:, 2] = np.cos(v_polar[:, 0] * np.pi)

        self.vrms = np.sqrt(3 * k_B * self.T / self.MASS)  # RMS VELOCITY
        self.v *= self.vrms

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
        if self.T == T:
            return
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

    def get_velocities(self):
        return np.sqrt(mod(self.r))

    def get_histogram(self):
        hist = np.array([])
        vel = self.get_velocities()
        for i in range(self.bin_count):
            bin = np.count_nonzero(
                (i * self.bin_width < vel) & (vel < (i + 1) * self.bin_width)
            )
            hist = np.append(hist, bin)
        return hist

    def save_object(self, filename="data.pkl"):
        with open(filename, "wb") as f:
            pickle.dump(self, f, pickle.HIGHEST_PROTOCOL)

    def load_object(filename="data.pkl"):
        with open(filename, "rb") as f:
            return pickle.load(f)
