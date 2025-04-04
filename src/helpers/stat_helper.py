from typing import List, Dict
import math

class StatHelper:

    @staticmethod
    def mean(arr: List[float]) -> float:
        if not arr:
            return float('nan')
        return sum(arr) / len(arr)

    @staticmethod
    def stddev(arr: List[float]) -> float:
        if not arr:
            return float('nan')
        avg = StatHelper.mean(arr)
        variance = sum((x - avg) ** 2 for x in arr) / len(arr)
        return math.sqrt(variance)

    @staticmethod
    def quantile(arr: List[float], q: float) -> float:
        if not 0 <= q <= 1:
            raise ValueError("Le quantile doit être entre 0 et 1.")
        if not arr:
            return float('nan')

        sorted_arr = sorted(arr)
        index = (len(sorted_arr) - 1) * q

        if index.is_integer():
            return sorted_arr[int(index)]
        lower = int(math.floor(index))
        upper = int(math.ceil(index))
        return (sorted_arr[lower] + sorted_arr[upper]) / 2

    @staticmethod
    def calculate_stats(arr: List[float]) -> Dict[str, float]:
        return {
            "mean": StatHelper.mean(arr),
            "stddev": StatHelper.stddev(arr),
            "min": min(arr) if arr else float('nan'),
            "max": max(arr) if arr else float('nan'),
            "quartiles": {
                "Q1": StatHelper.quantile(arr, 0.25),
                "median": StatHelper.quantile(arr, 0.5),
                "Q3": StatHelper.quantile(arr, 0.75),
            }
        }
