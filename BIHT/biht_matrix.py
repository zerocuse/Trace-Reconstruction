import numpy as np


def sign(x):
    return np.where(x >= 0, 1, -1)


def project_binary_symmetric(S):
    """Project a real matrix S onto the set of binary symmetric {0,1} matrices"""
    S_sym = (S + S.T) / 2
    X = np.sign(S_sym)
    X[X < 0] = 0
    return X


def biht_matrix(A, B, Y, iterations=100, eta=0.1):
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
