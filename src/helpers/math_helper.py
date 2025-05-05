import numpy as np

class MathHelper:
    @staticmethod
    def generate_range(n: int) -> list[int]:
        return list(range(1, n + 1))

    @staticmethod
    def euclidean_distance(a, b):
        return np.hypot(a[0] - b[0], a[1] - b[1])