from pprint import pprint

import numpy as np


class NonogramSolver:
    def __init__(self, field, x_hints, y_hints):
        self.field: np.ndarray = field
        self.x_hints = x_hints
        self.y_hints = y_hints

    @staticmethod
    def generate_configurations(l, hints):
        f = l - sum(hints) - len(hints)+1
        result = np.zeros((len(hints)+1,), dtype=np.int16)
        result[-1] = f
        yield result.copy()
        while result[0] < f:
            for pos, n in enumerate(result[1:]):
                if n > 0:
                    result[pos] += 1
                    result[pos+1] -= 1
                    if pos > 0:
                        result[pos] += result[0]
                        result[0] = 0
                    break
            yield result.copy()

    @staticmethod
    def check_configuration(row: np.ndarray, hints, configuration):
        p = 0
        if (row[:configuration[0]] == 1).any():
            return False
        else:
            p += configuration[0]
        for pos, h in enumerate(hints):
            if (row[p: p+h] == 0).any():
                return False
            else:
                p += hints[pos]
            if (row[p: p+configuration[pos+1]+1] == 1).any():
                return False
            else:
                p += configuration[pos+1]+1
        return True

    @staticmethod
    def get_configuration(l, hints, configuration):
        row = np.zeros(l, dtype=np.bool_)
        p = configuration[0]
        for pos, h in enumerate(hints):
            row[p: p+h] = 1
            p += h + configuration[pos+1] + 1
        return row

    @staticmethod
    def get_known_values(row, hints):
        l = len(row)
        known_set = row == -1
        known_not_set = known_set.copy()
        for c in NonogramSolver.generate_configurations(l, hints):
            if NonogramSolver.check_configuration(row, hints, c):
                v = NonogramSolver.get_configuration(l, hints, c)
                known_set &= v
                known_not_set &= np.invert(v)
            if not (known_set.any() or known_not_set.any()):
                break
        row[known_set] = 1
        row[known_not_set] = 0

    def is_solved(self):
        return not (self.field == -1).any()

    def solve(self):
        while not self.is_solved():
            for n, r in enumerate(self.field):
                NonogramSolver.get_known_values(r, self.y_hints[n])
            for n, r in enumerate(self.field.T):
                NonogramSolver.get_known_values(r, self.x_hints[n])


def solve_10x10(hints_y, hints_x):
    f_ = np.full((10, 10), -1, dtype=np.int16)
    n__ = NonogramSolver(f_, hints_x, hints_y)
    n__.solve()
    return n__.field