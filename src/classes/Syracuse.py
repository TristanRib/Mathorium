from enum import Enum
from typing import List


class Method(Enum):
    NORMAL = "normal"
    COMPRESSED = "compressed"


class SyracuseSuite:
    def __init__(self, suite: List[int]):
        self.suite = suite
        self.initial_value = suite[0]

    @property
    def fly_time(self) -> int:
        return len(self.suite) - 1

    @property
    def alt_fly_time(self) -> int:
        return next((i for i, val in self.suite if val < self.initial_value), self.fly_time)

    @property
    def max_alt(self) -> int:
        return max(self.suite)


class Syracuse:
    @staticmethod
    def _recursive(n: int, method: Method) -> List[int]:
        suite = [n]
        while n > 1:
            if method == Method.NORMAL:
                n = n // 2 if n % 2 == 0 else n * 3 + 1
            elif method == Method.COMPRESSED:
                n = n // 2 if n % 2 == 0 else (n * 3 + 1) // 2
            suite.append(n)
        return suite

    @staticmethod
    def generate_suite(n: int, method: Method = Method.NORMAL, inverse: bool = False) -> SyracuseSuite:
        suite = Syracuse._recursive(n, method)
        return SyracuseSuite(suite)
