import numpy as np
import scipy
from scipy.optimize import minimize, NonlinearConstraint

from sshist import sshist

def EMOT(x, y, opts=None):
    # Default options
    default_opts = {
        'thr': 0.10,
        'adjLastClick': True,
        'binHist': 22,
        'F0iidtol': 0.01,
        'verbose': True,
        'maxFunEvals': 25000,
        'maxIter': 25000,
        'display': 'none',
        'algorithm': 'interior-point',
        'sa_Tmin': 14,
        'sa_Tmax': 62
    }

    if opts is None:
        opts = default_opts

    if opts['verbose']:
        print('@ EMOT started')

    # Filtering coordinates near the starting point
    xraw = x.copy()
    yraw = y.copy()
    y[y <= opts['thr']] = np.nan
    x[np.isnan(y)] = np.nan
    x = x[~np.isnan(x)]
    y = y[~np.isnan(y)]

    try:
        # Computing radians from xy coordinates
        pols = np.angle(x + 1j * y)
        rescaled_pols = np.mod(pols + 2 * np.pi - np.pi, 2 * np.pi)
        theta = rescaled_pols

        lastClick = np.angle(x[-1] + 1j * y[-1]) + 2 * np.pi - np.pi
        lastClick = np.mod(lastClick, 2 * np.pi)

        if opts['adjLastClick']:
            theta = theta[theta != lastClick]

        if isinstance(opts['binHist'], int):
            xHist = np.linspace(0, np.pi, opts['binHist'] + 1)
        elif opts['binHist'] == 'auto':
            # Use the sshist function provided in the previous answer
            binHist = sshist(theta, np.arange(18, 71))
            if binHist % 2 == 1:
                binHist -= 1
            xHist = np.linspace(0, np.pi, binHist + 1)
        elif opts['binHist'] == 'sa':
            # Implement the sensAnalyHist function
            pass

        H_theta, _ = np.histogram(theta, bins=xHist)

        # Entropy decomposition
        theta0 = np.unique(np.round(theta / opts['F0iidtol'])) * opts['F0iidtol']
        H_theta0, _ = np.histogram(theta0, bins=xHist)

        # Call entropy decomposition routine
        # Implement the eDecomposition function
        res = {}

        # Save other information
        res['xref'] = x
        res['yref'] = y
        res['theta'] = theta
        res['theta0'] = theta0

        if opts['verbose']:
            print('@ EMOT finished')

    except Exception as e:
        if opts['verbose']:
            print('@ EMOT finished: An error occurred. Trajectories must be disregarded.')
        res = {}
        res['xref'] = np.nan
        res['yref'] = np.nan
        res['theta'] = np.nan
        res['theta0'] = np.nan

    return res