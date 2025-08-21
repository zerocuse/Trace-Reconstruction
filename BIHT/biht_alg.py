import numpy as np


def sign(x):
    return np.where(x >= 0, 1, -1)


def hard_thresholding(x, k):
    """Keep the top-k absolute entries and zero out the rest"""
    out = np.zeros_like(x)
    idx = np.argpartition(np.abs(x), -k)[-k:]
    out[idx] = x[idx]
    return out


def biht(A, y, k, iterations=100, eta=np.sqrt(2*np.pi)):
    """
    Binary Iterative Hard Thresholding (BIHT)

    Args:
        A: measurement matrix (m x n)
        y: 1-bit measurements (+1/-1), shape (m,)
        k: sparsity level
        iterations: number of iterations
        eta: step size

    Returns:
        Recovered signal (n,)
    """
    m, n = A.shape

    # Initialize x_hat: random unit vector with k non-zero entries
    x_hat = np.zeros(n)
    idx = np.random.choice(n, k, replace=False)
    x_hat[idx] = np.random.randn(k)
    x_hat /= np.linalg.norm(x_hat)

    for t in range(iterations):
        # Gradient-like step
        grad = (eta / (2 * m)) * A.T @ (y - sign(A @ x_hat))
        x_temp = x_hat + grad

        # Hard thresholding and renormalization
        x_hat = hard_thresholding(x_temp, k)
        x_hat /= np.linalg.norm(x_hat)

    return x_hat


# TEST EXAMPLE

n = 100          # signal dimension
k = 5            # sparsity
m = 80           # number of measurements

# Ground-truth sparse signal
x_true = np.zeros(n)
nonzero_idx = np.random.choice(n, k, replace=False)
x_true[nonzero_idx] = np.random.randn(k)
x_true /= np.linalg.norm(x_true)
print(x_true)

# Random measurement matrix
A = np.random.randn(m, n)

# 1-bit measurements
y = sign(A @ x_true)

# Recovery
x_rec = biht(A, y, k, iterations=100, eta=2.5)

# Check recovery quality
cosine_similarity = np.dot(x_rec, x_true)
print(f"Cosine similarity between true and recovered x: {cosine_similarity:.4f}")
