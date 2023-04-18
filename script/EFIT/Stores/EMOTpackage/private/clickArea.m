function [pars] = clickArea(X,Y,NUM_MVS)

if isempty(NUM_MVS), NUM_MVS = computeNUM_MVS(X); end
    
%% Detecting last click xy points
for i=1:size(X,1)
    xEnd(i) = X(i,NUM_MVS(i));
    yEnd(i) = Y(i,NUM_MVS(i));
end

%% Computing clicking area parameters
pars.a = [max(xEnd) max(yEnd)];
pars.b = [max(xEnd) min(yEnd)];
pars.c = [min(xEnd) min(yEnd)];
pars.d = [min(xEnd) max(yEnd)];


end