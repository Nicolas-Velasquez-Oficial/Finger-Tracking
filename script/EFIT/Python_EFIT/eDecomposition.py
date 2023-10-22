import numpy as np
from scipy.optimize import minimize, NonlinearConstraint

def e_decomposition(H_theta, H_theta0, xH, opts):
    # Computing PSI
    phi_omega = np.cumsum(H_theta / np.sum(H_theta))
    psi = -np.sum((1 - phi_omega) * np.log(1 - phi_omega + 1e-99))

    # Computing proxy for CSI, ZETA1, ZETA2
    pi = H_theta0 / np.sum(H_theta0) + 1e-99
    U = H_theta - H_theta0
    k = np.argwhere(xH == np.median(xH))
    if k.size == 0:
        raise ValueError('Error: BinHist must be an even number')
    U1 = U[:k[0][0]]
    U2 = U[k[0][0] + 1:]
    lambda1 = U1 / (np.sum(U1) + 1e-99) + 1e-99
    lambda2 = U2 / (np.sum(U2) + 1e-99) + 1e-99
    K = np.array([len(pi), len(lambda1), len(lambda2)])

    # Set parameters for the minimum KL-procedure
    q = np.concatenate((pi, lambda1, lambda2))
    p0 = np.ones(np.sum(K)) / K
    lb = np.ones(np.sum(K)) * 1e-99
    ub = np.ones(np.sum(K))

    # Minimum KL-procedure
    constraints = NonlinearConstraint(lambda p: H_cons(p, psi, K, np.sum(pi), np.sum(lambda1), np.sum(lambda2)), 0, 0)

    res = minimize(lambda p: H_function(p, q), p0, bounds=list(zip(lb, ub)), constraints=constraints, options=opts)

    if res.success:
        psi = psi
        tau = res.x[:K[0]]
        tau_star = np.cumsum(tau)
        u1 = res.x[K[0]:K[0] + K[1]]
        u1_star = np.cumsum(u1)
        u2 = res.x[K[0] + K[1]:]
        u2_star = np.cumsum(u2)

        csi = -np.sum((1 - tau_star) * np.log(1 - tau_star + 1e-99))
        zeta1 = -np.sum((1 - u1_star) * np.log(1 - u1_star + 1e-99))
        zeta2 = -np.sum((1 - u2_star) * np.log(1 - u2_star + 1e-99))

        return {
            'fail': False,
            'psi': psi,
            'tau': tau,
            'u1': u1,
            'u2': u2,
            'csi': csi,
            'zeta1': zeta1,
            'zeta2': zeta2,
            'zeta': zeta1 + zeta2,
            'H_theta': H_theta,
            'H_theta0': H_theta0,
            'xHist': xH,
            'U': U,
            'U1': U1,
            'U2': U2,
            'pi': pi,
            'lambda1': lambda1,
            'lambda2': lambda2,
            'thr': opts['thr']
        }
    else:
        return {'fail': True}

    def H_function(p, q):
        return np.sum(p * np.log((p + 1e-99) / (q + 1e-99)))

    def H_cons(p, psi, K, pi, lambda1, lambda2):
        tau = p[:K[0]]
        tau_star = np.cumsum(tau)
        u1 = p[K[0]:K[0] + K[1]]
        u1_star = np.cumsum(u1)
        u2 = p[K[0] + K[1]:]
        u2_star = np.cumsum(u2)

        csi = -np.sum((1 - tau_star) * np.log(1 - tau_star + 1e-99))
        zeta1 = -np.sum((1 - u1_star) * np.log(1 - u1_star + 1e-99))
        zeta2 = -np.sum((1 - u2_star) * np.log(1 - u2_star + 1e-99))

        ceq = np.zeros(4)
        ceq[0] = pi - np.sum(tau)
        ceq[1] = lambda1 - np.sum(u1)
        ceq[2] = lambda2 - np.sum(u2)
        ceq[3] = psi - csi - zeta1 - zeta2

        return ceq