from typing import Type
import numpy as np

from src.helpers.math_helper import MathHelper


class Cell:
    def __init__(self, position: tuple[float, float], radius: float = 3.0, signal_intensity=100):
        self.x, self.y = position
        self._radius = radius
        self._status = True

        jitter = np.random.uniform(1 - 0.05, 1 + 0.05)
        self._signal_intensity = signal_intensity * jitter

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
    def signalIntensity(self):
        return self._signal_intensity

    @signalIntensity.setter
    def signalIntensity(self, value):
        self._signal_intensity = value

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
        super().__init__(position, radius=3.0, signal_intensity=150)


class Lactose(Cell):
    def __init__(self, position: tuple[float, float]):
        super().__init__(position, radius=2.5, signal_intensity=80)


class AminoAcid(Cell):
    def __init__(self, position: tuple[float, float]):
        super().__init__(position, radius=2.0, signal_intensity=60)


class OxygenBubble(Cell):
    def __init__(self, position: tuple[float, float]):
        super().__init__(position, radius=2.5, signal_intensity=40)


class Bacteria(Cell):
    def __init__(self, position: tuple[float, float], nutrients: list[Type[Cell]], capture_factor: float = 1):
        super().__init__(position)
        self._nutrients = nutrients
        self._capture_factor = capture_factor

    @property
    def nutrients(self) -> list[Type[Cell]]:
        return self._nutrients

    @nutrients.setter
    def nutrients(self, value: list[Type[Cell]]):
        self._nutrients = value

    def detect_signal(self, other_cell: Cell):
        if not other_cell.status:  # Si la cellule est morte, on ignore son signal
            return 0

        distance = MathHelper.euclidean_distance(self.position, other_cell.position)

        if distance == 0:
            return float('inf')

        signal_strength = other_cell.signalIntensity / (distance ** 2)
        captured_signal = signal_strength * self._capture_factor

        if captured_signal >= 0.1:
            return captured_signal
        return 0

    def move_hunt(self, neighbours: list[Cell]):
        signals = [
            (cell, self.detect_signal(cell))
            for cell in neighbours
            if cell != self and self.detect_signal(cell) > 0
        ]

        if signals:
            target = max(signals, key=lambda x: x[1])[0]
            dx, dy = ChimeAttraction.delta(self, target)
            self.position = (self.x + dx, self.y + dy)

            if MathHelper.euclidean_distance(self.position, target.position) < target.radius:
                target.status = False
        else:
            self.move_random()


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
