import numpy as np


def sign(x):
    return np.where(x >= 0, 1, -1)


def project_binary_symmetric(S):
    """Project a real matrix S onto the set of binary symmetric {0,1} matrices"""
    S_sym = (S + S.T) / 2
    X = np.sign(S_sym)
    X[X < 0] = 0
    return X


def biht_matrix(A, B, Y, iterations=100, eta=0.01):
    """
    Binary Iterative Hard Thresholding (Matrix version)

    Args:
        A: measurement matrix (m x n)
        B: bias matrix (m x n)
        Y: sign measurements (m x n), entries in {-1, +1}
        iterations: number of iterations
        eta: step size

    Returns:
        X_hat: binary symmetric {0,1} matrix (n x n)
    """
    n = A.shape[1]

    # Initialize X_hat as a random binary symmetric matrix
    X_hat = np.random.randint(0, 2, size=(n, n))
    X_hat = np.triu(X_hat)  # upper triangle
    X_hat = X_hat + X_hat.T - np.diag(np.diag(X_hat))  # symmetrize

    for t in range(iterations):
        # Gradient step
        grad = 0.5 * A.T @ (sign(A @ X_hat + B) - Y)

        # Update and project
        X_hat = project_binary_symmetric(X_hat - eta * grad)

    return X_hat


# --- helper ---
def sign(x):
    return np.where(x >= 0, 1, -1)

# --- Ground-truth X from a real graph: C4 (cycle on 4 nodes) ---
# 1—2
# |  |
# 4—3
X_true = np.array([
    [0,1,0,1],
    [1,0,1,0],
    [0,1,0,1],
    [1,0,1,0]
], dtype=float)  # shape (4,4), binary symmetric

# --- Static measurement matrices (no randomness) ---
A = np.array([
    [ 1,  0, -1,  2],
    [ 0,  1,  1, -1],
    [ 2, -1,  0,  1]
], dtype=float)                                # shape (m=3, n=4)

B = np.array([
    [ 0.1, -0.5,  0.2,  0.0],
    [-0.3,  0.4, -0.1,  0.2],
    [ 0.0,  0.1, -0.2,  0.3]
], dtype=float)                                # shape (m=3, n=4)

# --- Static 1-bit measurements Y = sign(A @ X_true + B) ---
AX = A @ X_true                                # (3,4)
Y  = sign(AX + B)                              # (3,4)

print("X_true:\n", X_true)
print("\nA:\n", A)
print("\nB:\n", B)
print("\nA @ X_true:\n", AX)
print("\nY = sign(A @ X_true + B):\n", Y)
# Y equals:
# [[ 1, -1,  1,  1],
#  [-1,  1, -1,  1],
#  [ 1,  1, -1,  1]]

# ===== Run your matrix BIHT here =====
# Assumes you already defined:
#   - project_binary_symmetric(S)
#   - biht_matrix(A, B, Y, iterations=..., eta=...)

np.random.seed(0)  # for reproducible initialization inside BIHT
X_rec = biht_matrix(A, B, Y, iterations=100, eta=0.1)

print("\nRecovered X_rec:\n", X_rec)
acc = np.mean(X_rec == X_true)
print(f"\nEntry-wise accuracy: {acc:.2%}")
