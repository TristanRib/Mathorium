import numpy as np

from src.helpers.math_helper import MathHelper
from src.projects.Chemotaxis.classes.Cell import Cell


class ChimeAttraction:
    @staticmethod
    def delta(source: Cell, target: Cell, step=1, mu=0, sigma=2 * np.pi):
        angle = np.random.uniform(mu, sigma)

        source_position = source.body.get_position(source)
        target_position = source.body.get_position(target)

        if np.random.normal(0, 1) < ChimeAttraction.turn_probability(source_position, target_position):
            dx = target_position[0] - source_position[0]
            dy = target_position[1] - source_position[1]

            angle_parfait = np.arctan2(dy, dx)
            noise = np.random.normal(0, np.pi / 6)

            angle = angle_parfait + noise

        return step * np.cos(angle), step * np.sin(angle)

    @staticmethod
    def turn_probability(a, b):
        c = 1 / (1 + MathHelper.euclidean_distance(a, b))
        k = 5.0
        p = 0.30
        return p * np.exp(-k * c)
