from scipy.linalg import solve
import numpy as np

A = np.array([[3, 1], [1, 2]])
b = np.array([9, 8])

x = solve(A, b)
print("Solution:", x)
