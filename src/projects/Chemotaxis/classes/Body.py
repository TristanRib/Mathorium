import numpy as np
from typing import Type

from src.projects.Chemotaxis.classes.Bacteria import Bacteria
from src.projects.Chemotaxis.classes.Cell import Cell


class Body:
    def __init__(self, cell_specs: list[tuple[Type[Cell], int]], size: int = 256):
        self._size = size

        self._cells: dict[Cell, tuple[float, float]] = {}

        for cell_class, count in cell_specs:
            for _ in range(count):
                x = np.random.uniform(-size / 2, size / 2)
                y = np.random.uniform(-size / 2, size / 2)
                cell = cell_class()
                self._cells[cell] = (x, y)
                cell.body = self

    @property
    def size(self) -> int:
        return self._size

    @property
    def cells(self) -> dict[Cell, tuple[float, float]]:
        return self._cells

    @cells.setter
    def cells(self, value: dict[Cell, tuple[float, float]]):
        self._cells = value

    def get_position(self, cell):
        return self.cells[cell]

    def update_position(self, cell, delta):
        current_x, current_y = self.cells[cell]
        dx, dy = delta
        new_x = max(-self._size, min(self._size, current_x + dx))
        new_y = max(-self._size, min(self._size, current_y + dy))
        self.cells[cell] = (new_x, new_y)

    def chemotaxis(self, t=42):
        positions = {cell: [self.get_position(cell)] for cell in self.cells}

        for i in range(t):
            for cell in self.cells:
                if cell.status:
                    if isinstance(cell, Bacteria):
                        cell.move_hunt()
                    elif isinstance(cell, Cell):
                        cell.move_random()

                positions[cell].append(cell.body.get_position(cell))
        return positions
