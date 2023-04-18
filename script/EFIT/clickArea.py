import computeNUM_MVS

def clickArea(X, Y, NUM_MVS=None):
    if NUM_MVS is None:
        NUM_MVS = computeNUM_MVS(X)

    # Detecting last click xy points
    xEnd = X[:, NUM_MVS - 1]
    yEnd = Y[:, NUM_MVS - 1]

    # Computing clicking area parameters
    pars = {}
    pars['a'] = [max(xEnd), max(yEnd)]
    pars['b'] = [max(xEnd), min(yEnd)]
    pars['c'] = [min(xEnd), min(yEnd)]
    pars['d'] = [min(xEnd), max(yEnd)]

    return pars