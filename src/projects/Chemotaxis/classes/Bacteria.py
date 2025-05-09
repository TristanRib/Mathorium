from typing import Type

from src.helpers.math_helper import MathHelper
from src.projects.Chemotaxis.classes.Cell import Cell, Glucose, AminoAcid, OxygenBubble
from src.projects.Chemotaxis.classes.Chemotaxis import ChimeAttraction


class Bacteria(Cell):
    def __init__(self, nutrients: list[Type[Cell]], capture_factor: float = 1):
        super().__init__()
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

        distance = MathHelper.euclidean_distance(self._body.get_position(self), self._body.get_position(other_cell))

        if distance == 0:
            return float('inf')

        signal_strength = other_cell.signal_intensity / (distance ** 2)
        captured_signal = signal_strength * self._capture_factor

        return captured_signal

    def move_hunt(self):
        # On capte tous les signaux des autres cellules du corps
        signals = [
            (cell, self.detect_signal(cell))
            for cell in self._body.cells
            if cell != self and self.detect_signal(cell) > 0
        ]
        # On trie pour les signaux des cellules que l'on chasse
        nutrient_signals = [
            (cell, signal)
            for cell, signal in signals
            if isinstance(cell, tuple(self.nutrients))
        ]

        if nutrient_signals:
            target = max(nutrient_signals, key=lambda x: x[1])[0]
            dx, dy = ChimeAttraction.delta(self, target)
            self._body.update_position(self, (dx, dy))

            # On tue la cellule si on l'attrape
            if MathHelper.euclidean_distance(self._body.get_position(self),
                                             self._body.get_position(target)) < target.radius:
                target.status = False
        else:
            self.move_random()


class EscherichiaColy(Bacteria):
    def __init__(self):
        super().__init__([Glucose, AminoAcid, OxygenBubble])
