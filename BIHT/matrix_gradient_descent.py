import numpy as np


# ---------- HELPERS ----------


def sign_pm1(x):
    return np.where(x >= 0, 1, -1)


def project_binary_symmetric_topk(S, k):
    S = 0.5 * (S + S.T)  # symmetrize scores
    n = S.shape[0]

    # work on strict upper triangle
    iu = np.triu_indices(n, k=1)
    scores = S[iu]
    k_half = int(k // 2)
    k_half = max(0, min(k_half, scores.size))

    # pick indices of top k_half scores
    if k_half > 0:
        keep_idx = np.argpartition(scores, -k_half)[-k_half:]
    else:
        keep_idx = np.array([], dtype=int)

    X = np.zeros((n, n), dtype=int)
    X[iu[0][keep_idx], iu[1][keep_idx]] = 1
    X = X + X.T  # mirror to keep symmetry
    return X


# ---------- MATRIX BIHT ----------


def biht_matrix_slide(A, B, Y, k, iterations=500, eta=.01, seed=0):
    rng = np.random.default_rng(seed)
    n = A.shape[1]

    # random init, then project to feasible set (|X|_1 = k)
    S0 = rng.standard_normal((n, n))
    X = project_binary_symmetric_topk(S0, k)

    # spectral-norm step size if not provided
    if eta is None:
        s = np.linalg.norm(A, 2)  # spectral norm of A
        eta = 1.0 / (2.0 * (s ** 2 + 1e-12))

    for _ in range(iterations):
        G = 0.5 * A.T @ (sign_pm1(A @ X + B) - Y)
        X = project_binary_symmetric_topk(X - eta * G, k)

    return X


# ---------- TEST CASE ----------


if __name__ == "__main__":
    np.set_printoptions(linewidth=120, suppress=True)

    # Ground-truth X
    X_true = np.array([
        [0, 1, 0, 1],
        [1, 0, 1, 0],
        [0, 1, 0, 1],
        [1, 0, 1, 0]
    ], dtype=float)

    # Measurement matrices
    A = np.array([
        [1, 0, -1, 2],
        [0, 1, 1, -1],
        [2, -1, 0, 1]
    ], dtype=float)

    B = np.array([
        [0.1, -0.5, 0.2, 0.0],
        [-0.3, 0.4, -0.1, 0.2],
        [0.0, 0.1, -0.2, 0.3]
    ], dtype=float)

    # 1-bit measurements
    AX = A @ X_true
    Y = sign_pm1(AX + B)

    print("X_true:\n", X_true.astype(int))
    print("\nY = sign(A @ X_true + B):\n", Y)

    # Run BIHT
    k = int(X_true.sum())  # total number of ones in X_true
    X_rec = biht_matrix_slide(A, B, Y, k=k, iterations=1000, eta=5, seed=8)

    print("\nRecovered X_rec:\n", X_rec)
    acc = np.mean(X_rec == X_true)
    print(f"\nEntry-wise accuracy: {acc:.2%}")
    print("\n|X_rec|_1 (should equal k):", int(X_rec.sum()))
    print("Symmetry check (||X - X^T||_1):", int(np.abs(X_rec - X_rec.T).sum()))
