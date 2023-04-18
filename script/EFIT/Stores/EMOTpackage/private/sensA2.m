function [] = sensA2()

opts.thr=0.1;
opts.F0iidtol = 0.005;
opts.maxFunEvals = 25000;
opts.maxIter = 25000;
opts.verbose = false;

Tmin=10; Tmax=60;

Ts = round(random('uniform',Tmin,Tmax,1,1))


end