import numpy as np
def matrixmul(a: list[list[int|float]], b: list[list[int|float]]) -> list[list[int|float]]:
    # a is m x n, b is n x p — need columns of a == rows of b
    if len(a[0]) != len(b):
        return -1
    return np.matmul(a, b)