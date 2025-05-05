from typing import Type
import numpy as np

from src.helpers.math_helper import MathHelper


class Cell:
    def __init__(self, position: tuple[float, float], radius: float = 3.0):
        self.x, self.y = position
        self._radius = radius
        self._status = True

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = value

    @property
    def position(self):
        return self.x, self.y

    @position.setter
    def position(self, value):
        self.x, self.y = value

    @property
    def radius(self) -> float:
        return self._radius

    @radius.setter
    def radius(self, value):
        self._radius = value

    def move_random(self, step=1):
        angle = np.random.uniform(0, 2 * np.pi)
        dx = step * np.cos(angle)
        dy = step * np.sin(angle)
        self.position = (self.x + dx, self.y + dy)


class Glucose(Cell):
    def __init__(self, position: tuple[float, float]):
        super().__init__(position)


class Bacteria(Cell):
    def __init__(self, position: tuple[float, float], nutrients: list[Type[Cell]]):
        super().__init__(position)
        self._nutrients = nutrients

    @property
    def nutrients(self) -> list[Type[Cell]]:
        return self._nutrients

    @nutrients.setter
    def nutrients(self, value: list[Type[Cell]]):
        self._nutrients = value

    def move_hunt(self, neighbours: list[Cell]):
        valid_targets = [
            target for target in neighbours
            if isinstance(target, tuple(self.nutrients)) and target.status
        ]

        if valid_targets:
            closest_target = min(
                valid_targets,
                key=lambda target: MathHelper.euclidean_distance(self.position, target.position)
            )

            dx, dy = ChimeAttraction.delta(self, closest_target)
            self.position = (self.x + dx, self.y + dy)

            if MathHelper.euclidean_distance(self.position, closest_target.position) < closest_target.radius:
                closest_target.status = False


class EscherichiaColy(Bacteria):
    def __init__(self, position: tuple[float, float]):
        super().__init__(position, [Glucose])


class Body:
    def __init__(self, cells: list[Cell]):
        self._cells = cells

    @property
    def cells(self) -> list[Cell]:
        return self._cells

    @cells.setter
    def cells(self, value: list[Cell]):
        self._cells = value

    def chemotaxis(self, t=42):
        positions = {cell: [cell.position] for cell in self.cells}

        for i in range(t):
            for cell in self.cells:
                if cell.status:
                    if isinstance(cell, Cell) and not isinstance(cell, Bacteria):
                        cell.move_random()
                    elif isinstance(cell, Bacteria):
                        cell.move_hunt(self.cells)

                positions[cell].append(cell.position)
        return positions


class ChimeAttraction:
    @staticmethod
    def delta(source: Cell, target: Cell, step=1, mu=0, sigma=2 * np.pi):
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
