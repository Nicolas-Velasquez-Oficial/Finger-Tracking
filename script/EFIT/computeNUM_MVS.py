import numpy as np
def computeNUM_MVS(X):
    NUM_MVS = []
    for i in range(X.shape[0]):
        NUM_MVS.append(max(np.where(X[i] != 0)[0]) + 1)
    return NUM_MVS