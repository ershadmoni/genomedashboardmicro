import numpy as np


class EnergyService:

    @staticmethod
    def compute_energy(vector, stiffness):

        vector = np.array(vector)

        energy = 0.5 * vector.T @ stiffness @ vector

        return float(energy)
