from typing import Type
import numpy as np

from src.helpers.math_helper import MathHelper


class Cell:
    pass


class Bacteria(Cell):
    def __init__(self, sources: list[Type[Cell]]):
        self.nutrientSource = sources

    def getNutrients(self):
        return self.nutrientSource

    def radius(self) -> float:
        return 3.0

class FastFood(Bacteria):
    def __init__(self):
        super().__init__([])


class EscherichiaColy(Bacteria):
    def __init__(self):
        super().__init__([FastFood])


class Body:
    def __init__(self, cells: list[tuple[Cell, tuple[float, float]]]):
        self.cells = cells

    def getCells(self):
        return self.cells

    def chemotaxis(self, t=42):
        for cell in self.cells:
            positions = [cell[1]]

            for i in range(t):
                current_pos = self.position
                closest_target = min(targets,
                                     key=lambda target: MathHelper.euclidean_distance(current_pos, target.position))
                if MathHelper.euclidean_distance(current_pos, closest_target.position) <= closest_target.radius():
                    print(f"Target atteinte à la position {current_pos} en {i} mouvements !")

                dx, dy = ChimeAttraction.delta(self, closest_target)
                self.x += dx
                self.y += dy

                positions.append(self.position)

            print(f"Aucune target atteinte en {i} mouvements !")



class ChimeAttraction:
    @staticmethod
    def delta(source: EscherichiaColy, target: FastFood, step=1, mu=0, sigma=2 * np.pi):
        angle = np.random.uniform(mu, sigma)

        if np.random.normal(0, 1) < ChimeAttraction.turn_probability(source.position, target.position):
            dx = target.position[0] - source.position[0]
            dy = target.position[1] - source.position[1]

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
