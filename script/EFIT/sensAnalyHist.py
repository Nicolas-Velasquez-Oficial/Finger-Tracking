
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from EMOT import EMOT

def roundN(num, n):
    return round(num, n)

def quantile(arr, q):
    return np.quantile(arr, q)

def sens_analy_hist(x, y, Tmin, Tmax, fig, verbose):
    opts = {
        'thr': 0.1,
        'maxFunEvals': 25000,
        'maxIter': 25000,
        'verbose': False,
        'F0iidtol': 0.005
    }
    tOpt = 22

    y[y <= opts['thr']] = np.nan
    x[np.isnan(y)] = np.nan
    x = x[~np.isnan(x)]
    y = y[~np.isnan(y)]

    if verbose:
        print('@@ Optimizing T', end='')
    c = 0
    countNaN = 0
    D = []
    for k in range(Tmin, Tmax+1, 2):
        if verbose:
            print('.', end='')
        c += 1
        opts['binHist'] = k
        res = EMOT(x, y, opts) # You need to define or import EMOT function
        if np.isnan(res['fail']):
            countNaN += 1
        if not np.isnan(res['fail']):
            countNaN = 0
            D.append([k, 0, res['psi'], res['csi'], res['zeta1'], res['zeta2']])
        if countNaN > 3:
            break
    del res, opts

    D = np.array(D)
    C = np.column_stack([
        roundN(D[:, 4], 2) > roundN(D[:, 5], 2),
        roundN(D[:, 4], 2) < roundN(D[:, 5], 2),
        roundN(D[:, 4], 2) == roundN(D[:, 5], 2)
    ])
    _, f = np.max(np.sum(C, axis=0)), np.argmax(np.sum(C, axis=0))
    iid = C[:, f]
    Dd = D[iid.astype(bool), :]
    tBest = np.zeros(3)

    if np.median(Dd[:, 3]) > 0.1:
        tBest[0] = max(D[np.abs(Dd[:, 3] - np.median(Dd[:, 3])) == np.min(np.abs(Dd[:, 3] - np.median(Dd[:, 3]))), 0])
    if np.median(Dd[:, 4]) > 0.1:
        tBest[1] = max(D[np.abs(Dd[:, 4] - np.median(Dd[:, 4])) == np.min(np.abs(Dd[:, 4] - np.median(Dd[:, 4]))), 0])
    if np.median(Dd[:, 5]) > 0.1:
        tBest[2] = max(D[np.abs(Dd[:, 5] - np.median(Dd[:, 5])) == np.min(np.abs(Dd[:, 5] - np.median(Dd[:, 5]))), 0])

    tBest = tBest[tBest > 0]
    if len(tBest) > 0:
        tOpt = roundN(np.mean(tBest), 2)
        if tOpt % 2:
            tOpt -= 1
            accOpt = (np.sum(C[:, f]) / len(C[:, f])) * 100
        else:

            try:
                tOpt = max(
                    D[np.abs(Dd[:, 2] - np.median(Dd[:, 2])) == np.min(np.abs(Dd[:, 2] - np.median(Dd[:, 2]))), 0])
            except ValueError:
                tOpt = None
            accOpt = np.nan

        if verbose:
            print(f'done: {tOpt}({accOpt:.1f}%)')

        results = {
            'data': D,
            'T': tOpt,
            'acc': accOpt
        }

        if fig:
            plt.figure(1)
            plt.scatter(x, y)
            plt.axis([-1.2, 1.2, 0, 1.05])
            plt.axvline(0, linestyle='-.', linewidth=1, color='k')
            plt.plot(x[-1], y[-1], 'r.')

            hFig, axs = plt.subplots(2, 2, figsize=(10, 6))
            hFig.set_facecolor([0.8, 0.8, 0.8])

            axs[1, 1].scatter(Dd[:, 0], Dd[:, 5], color='b', marker='.')
            axs[1, 1].plot(Dd[:, 0], Dd[:, 5], 'b-')
            axs[1, 1].axhline(np.mean(Dd[:, 5]), linestyle='-.', linewidth=2, color='r')
            axs[1, 1].axhline(np.median(Dd[:, 5]), linestyle='-.', linewidth=2, color='g')
            axs[1, 1].axhline(quantile(Dd[:, 5], 0.95), linestyle='-.', linewidth=2, color='k')
            axs[1, 1].axhline(quantile(Dd[:, 5], 0.05), linestyle='-.', linewidth=2, color='k')
            axs[1, 1].set_title(r'$\fontsize{17} \bf \upsilon_2$')

            # Similar plots for the other subplots (axs[1, 0], axs[0, 1], and axs[0, 0])
            # ...
            # ...

            plt.show()

        return results