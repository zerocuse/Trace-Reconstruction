import numpy as np

# RANDOM SEED
np.random.seed(0)

X_true = np.array([
    [0, 1, 0, 0, 1],
    [1, 0, 1, 0, 0],
    [0, 1, 0, 0, 0],
    [0, 0, 0, 0, 1],
    [1, 0, 0, 1, 0]
])

# NODES / MEASUREMENTS
m = 6
n = 5

# Inputs: lambda_reg, steps, eta
lambda_reg = 0.1  # sparsity weight
steps = 100
eta = 0.05

# CONSTRUCT A, B, Y
A = np.random.randn(m, n)
B = 0.2 * np.ones((m, n))
Z_true = A @ X_true + B
Y = np.sign(Z_true)

X = np.zeros((A.shape[1], A.shape[1]))  # init
for _ in range(steps):
    Z = A @ X + B
    mask = (np.sign(Z) != Y)  # entries where sign mismatch
    grad = A.T @ (mask * Y * (-1))      # subgradient of mismatches
    X -= eta * (grad + lambda_reg * np.sign(X))  # grad + L1 sparsity
    X = np.clip((X + X.T) / 2, 0, 1)    # symmetry + bounds
Xhat = (X > 0.5).astype(int)            # binarize
