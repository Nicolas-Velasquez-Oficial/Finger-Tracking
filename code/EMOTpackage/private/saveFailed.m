function [res] = saveFailed()

    res.fail = 1; res.psi = NaN; res.tau = NaN; res.u1 = NaN; res.u2 = NaN; res.csi = NaN; res.zeta1 = NaN; res.zeta2 = NaN; 
    res.zeta = NaN; res.H_theta = NaN; res.H_theta0 = NaN; res.xHist = NaN; res.U = NaN; res.U1 = NaN; res.U2 = NaN; res.pi = NaN;
    res.lambda1 = NaN; res.lambda2 = NaN; res.thr = NaN; res.KL_output = NaN; 

end