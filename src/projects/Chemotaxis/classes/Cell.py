import numpy as np


class Cell:
    def __init__(self, radius: float = 3.0, signal_intensity=100, signal_jitter=0.05):
        self._body = None
        self._radius = radius
        self._status = True
        # On met une petite imprécision sur les signaux pour de l'aléatoire
        self._signal_intensity = signal_intensity * np.random.uniform(1 - signal_jitter, 1 + signal_jitter)

    @property
    def body(self):
        return self._body

    @body.setter
    def body(self, value) -> None:
        self._body = value

    @property
    def status(self) -> bool:
        return self._status

    @status.setter
    def status(self, value: bool) -> None:
        self._status = value

    @property
    def signal_intensity(self) -> float:
        return self._signal_intensity

    @signal_intensity.setter
    def signal_intensity(self, value) -> None:
        self._signal_intensity = value

    @property
    def radius(self) -> float:
        return self._radius

    @radius.setter
    def radius(self, value) -> None:
        self._radius = value

    def move_random(self, step=1) -> None:
        angle = np.random.uniform(0, 2 * np.pi)
        dx = step * np.cos(angle)
        dy = step * np.sin(angle)
        self._body.update_position(self, (dx, dy))


class Glucose(Cell):
    def __init__(self):
        super().__init__(radius=3.0, signal_intensity=150)


class Lactose(Cell):
    def __init__(self):
        super().__init__(radius=2.5, signal_intensity=80)


class AminoAcid(Cell):
    def __init__(self):
        super().__init__(radius=2.0, signal_intensity=60)


class OxygenBubble(Cell):
    def __init__(self):
        super().__init__(radius=2.5, signal_intensity=40)
