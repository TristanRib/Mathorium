class Syracuse:
    """
    Hypothèse mathématique selon laquelle la suite de Syracuse de n'importe quel entier strictement positif atteint 1.
    """
    def __init__(self, number: int):
        self.number = number
        self.suite: list[int] = []

    def _recursive(self, n: int):
        self.suite.append(n)
        if n > 1:
            next_n = n // 2 if n % 2 == 0 else n * 3 + 1
            self._recursive(next_n)

    def generate_suite(self) -> list[int]:
        self.suite = []
        self._recursive(self.number)
        return self.suite

    @property
    def fly_time(self) -> int:
        return len(self.suite) - 1

    @property
    def alt_fly_time(self) -> int:
        for i, val in enumerate(self.suite):
            if val < self.number:
                return i
        return self.fly_time

    @property
    def max_alt(self) -> int:
        return max(self.suite)