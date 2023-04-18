%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% EMOT Package v.1.0 (2016/04/25)                                                    
% by Antonio Calcagnì
% Dep. of Psychology and Cognitive Science, University of Trento (Italy)
% email: ant.calcagni@gmail.com
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

function [res] = eDecomposition(H_theta,H_theta0,xH,opts)
warning off

%% Computing PSI
phi_omega = cumsum(H_theta./sum(H_theta));
psi = real(-sum((1-phi_omega).*log(1-phi_omega+1e-99)));

%% Computing proxy for CSI, ZETA1, ZETA2
pi = H_theta0./sum(H_theta0)+1e-99;
U = H_theta-H_theta0;
k = find(xH==median(xH)); if isempty(k), error('Error: BinHist must be an even number'), end
U1 = zeros(length(H_theta(1:k-1)),1); U1 = U(1:k-1);
U2 = zeros(length(H_theta(k+1:end)),1); U2 = U(k+1:end);
lambda1 = U1./(sum(U1)+1e-99)+1e-99;
lambda2 = U2./(sum(U2)+1e-99)+1e-99;
K = [length(pi) length(lambda1) length(lambda2)];

%% Set parameters for the minimum KL-procedure
%K = length(pi);
q = [pi;lambda1;lambda2];
p0 = [ones(K(1),1)*1/K(1);ones(K(2),1)*1/K(2);ones(K(3),1)*1/K(2)];
lb = ones(K(1)*3,1)*1e-99; 
ub = ones(K(1)*3,1);

options = optimset('MaxFunEvals',opts.maxFunEvals,'MaxIter',opts.maxIter,...
    'Display',opts.display,'Algorithm',opts.algorithm);

%% Minimum KL-procedure
[p,~,exitflag,output]=fmincon(@(p)H_Function(p,q),p0,[],[],[],[],lb,ub,@(p)H_cons(p,psi,K,sum(pi),sum(lambda1),sum(lambda2)),options);
fail=false;
if exitflag<=0, if opts.verbose, fprintf(2,'@@ e-Decomposition: Failed \n'.'), end, fail=true;
else if opts.verbose, fprintf(1,'@@ e-Decomposition: Successfully executed! \n'),end, end

%% Save results
if ~fail
    res.fail = fail;
    res.psi = psi;
    res.tau = p(1:K(1)); tau_star = cumsum(res.tau);
    res.u1 = p(K(1)+1:K(1)+K(2)); u1_star = cumsum(res.u1);
    res.u2 = p(K(1)+K(2)+1:end); u2_star = cumsum(res.u2);
    res.csi = real(-sum((1-tau_star).*log(1-tau_star+1e-99)));
    res.zeta1 = real(-sum((1-u1_star).*log(1-u1_star+1e-99)));
    res.zeta2 = real(-sum((1-u2_star).*log(1-u2_star+1e-99)));    
    res.zeta = res.zeta1 + res.zeta2;
    res.H_theta = H_theta;
    res.H_theta0 = H_theta0;
    res.xHist = xH;
    res.U = U;
    res.U1 = U1;
    res.U2 = U2;
    res.pi = pi;
    res.lambda1 = lambda1;
    res.lambda2 = lambda2;
    res.thr = opts.thr;
    res.KL_output = output;
else
    res = saveFailed();
end

warning on
end

%% KL-divergence function
function [H] = H_Function(p,q), H = real(sum(p.*log(p./q+1e-99)));end

%% Constrains function
function [c,ceq]=H_cons(p,psi,K,pi,lambda1,lambda2)

tau = p(1:K(1)); tau_star = cumsum(tau);
u1 = p(K(1)+1:K(1)+K(2)); u1_star = cumsum(u1);
u2 = p(K(1)+K(2)+1:end); u2_star = cumsum(u2);

csi = real(-sum((1-tau_star).*log(1-tau_star+1e-99)));
zeta1 = real(-sum((1-u1_star).*log(1-u1_star+1e-99)));
zeta2 = real(-sum((1-u2_star).*log(1-u2_star+1e-99)));

ceq(1) = real(pi-sum(tau));
ceq(2) = real(lambda1-sum(u1));
ceq(3) = real(lambda2-sum(u2));
ceq(4) = real(psi-csi-zeta1-zeta2);

c=[];
end