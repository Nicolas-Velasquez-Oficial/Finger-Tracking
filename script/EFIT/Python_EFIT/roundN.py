import numpy as np

def roundsd(x, n, method='round'):
    if not isinstance(x, (int, float, np.ndarray)):
        raise ValueError("X argument must be numeric.")

    if not isinstance(n, int) or n < 0:
        raise ValueError("N argument must be a scalar positive integer.")

    opt = {'round', 'floor', 'ceil', 'fix'}

    if method not in opt:
        raise ValueError("METHOD argument is invalid.")

    e = np.floor(np.log10(np.abs(x)) - n + 1)
    og = np.power(10, np.abs(e))

    if method == 'round':
        y = np.round(x / og) * og
    elif method == 'floor':
        y = np.floor(x / og) * og
    elif method == 'ceil':
        y = np.ceil(x / og) * og
    elif method == 'fix':
        y = np.fix(x / og) * og

    k = np.where(e < 0)
    if k[0].size > 0:
        if method == 'round':
            y[k] = np.round(x[k] * og[k]) / og[k]
        elif method == 'floor':
            y[k] = np.floor(x[k] * og[k]) / og[k]
        elif method == 'ceil':
            y[k] = np.ceil(x[k] * og[k]) / og[k]
        elif method == 'fix':
            y[k] = np.fix(x[k] * og[k]) / og[k]

    y[x == 0] = 0

    return y