import numpy as np
import pandas as pd
import time
from scipy.optimize import minimize, NonlinearConstraint
from EMOT import EMOT
from computeNUM_MVS import computeNUM_MVS
from clickArea import clickArea
from plot_Results import plot_Results



def EMOT_main(X, Y, analysis, graphic, saveFileName, options):
    # Useful parameters
    if 'NUM_MVS' not in locals():
        NUM_MVS = computeNUM_MVS(X)
    if 'RTS' in locals():
        time = [0, 0]
    else:
        time = [0, 0]
    try:
        outs = eval('outs')
    except:
        outs = []
    g = list(map(int, str(analysis[1]).split()))
    if saveFileName:
        fileName = saveFileName
    else:
        fileName = 'EMOT.results'

    # EMOT routine
    print('\n==================== EMOT v.1.0 ==================================')
    res = []
    if analysis[0] == 'single':
        i = g[0]
        print('\n@ Single trial analysis: Data id. ' + str(i))
        x = X[i, 0:NUM_MVS[i]]
        y = Y[i, 0:NUM_MVS[i]]
        res = EMOT(x, y, options)
        if graphic and not res['fail']:
            X0 = X
            Y0 = Y
            X0 = np.delete(X0, outs, axis=0)
            Y0 = np.delete(Y0, outs, axis=0)
            pars = clickArea(X0, Y0, NUM_MVS)
            names = ['', '', '']
            plot_Results(X[i, 0:NUM_MVS[i]], Y[i, 0:NUM_MVS[i]], res, pars, i, names, time)

    elif analysis[0] == 'group':
        for i in range(g[0], g[1] + 1):
            print('\n@ Group analysis: Data id. ' + str(i))
            res.append(EMOT(X[i, 0:NUM_MVS[i]], Y[i, 0:NUM_MVS[i]], options))
            tosave = np.concatenate(([i], [res[i]['psi'], res[i]['csi'], res[i]['zeta1'], res[i]['zeta2']]))
        np.savetxt(fileName + '_' + time.strftime('%Y%m%d') + '_' + time.strftime('%H%M%S') + '.csv', tosave)
        np.save(fileName + '_' + time.strftime('%Y%m%d') + '_' + time.strftime('%H%M%S') + '.npy', res)

    print('\n==================================================================')

    return res

    data = pd.read_csv("prosocial_data.csv")

    def str_to_array(list_string):
        # converts a list that is surrounded by quotes to a numpy array
        # e.g. "[0,1,2,3]" to array([0,1,2,3])
        str_split = list_string.split(",")
        first_ele = float(str_split[0].replace("[", ""))
        last_ele = float(str_split[-1].replace("]", ""))
        other_ele = np.array(list(str_split)[1:-1], dtype=float)
        all_ele = np.insert(other_ele, 0, first_ele)
        all_ele = np.append(all_ele, last_ele)
        return all_ele

    x = data.loc[0,'xmouse']
    y = data.loc[0,'ymouse']

    arrayx = str_to_array(x)
    arrayy = str_to_array(y)

    EMOT_main(arrayx, arrayy,{'single', 1},"true",[],"opts")

