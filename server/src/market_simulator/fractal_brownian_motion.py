import numpy as np


def fractional_brownian_motion(H, N, T=1.0):
    """
    Simulate a fractional Brownian motion (fBm).

    Parameters:
        H (float): Hurst parameter (0 < H < 1).
        N (int): Number of steps.
        T (float): Total time (default 1.0).

    Returns:
        t (ndarray): Time grid.
        fbm (ndarray): Simulated fractional Brownian motion.
    """
    dt = T / N
    t = np.linspace(0, T, N + 1)

    # Covariance matrix for fractional Brownian motion
    def covariance(i, j):
        return 0.5 * (
            abs(i * dt) ** (2 * H)
            + abs(j * dt) ** (2 * H)
            - abs((i - j) * dt) ** (2 * H)
        )

    # Construct covariance matrix
    cov_matrix = np.zeros((N + 1, N + 1))
    for i in range(N + 1):
        for j in range(N + 1):
            cov_matrix[i, j] = covariance(i, j)

    # Cholesky decomposition
    L = np.linalg.cholesky(cov_matrix)

    # Generate random Gaussian vector
    z = np.random.normal(size=N + 1)

    # Simulate fBm
    fbm = np.dot(L, z)

    return t, fbm
