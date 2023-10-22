import numpy as np

def sshist(x, N=None):
    x = x.flatten()
    x_min = np.min(x)
    x_max = np.max(x)

    if N is None:
        buf = np.abs(np.diff(np.sort(x)))
        dx = np.min(buf[buf != 0])
        N_MIN = 2
        N_MAX = min(int(np.floor((x_max - x_min) / (2 * dx))), 500)
        N = np.arange(N_MIN, N_MAX + 1)

    SN = 30
    D = (x_max - x_min) / N

    Cs = np.zeros((len(N), SN))
    for i in range(len(N)):
        shift = np.linspace(0, D[i], SN)
        for p in range(SN):
            edges = np.linspace(x_min + shift[p] - D[i] / 2, x_max + shift[p] - D[i] / 2, N[i] + 1)
            ki = np.histogram(x, bins=edges)[0]
            k = np.mean(ki)
            v = np.sum((ki - k) ** 2) / N[i]
            Cs[i, p] = (2 * k - v) / D[i] ** 2

    C = np.mean(Cs, axis=1)
    Cmin, idx = np.min(C), np.argmin(C)
    optN = N[idx]
    optD = D[idx]
    edges = np.linspace(x_min, x_max, optN)

    return optN, optD, edges, C, N