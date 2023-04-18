%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% EMOT Package v.1.0 (2016/04/25)                                                    
% by Antonio Calcagnì
% Dep. of Psychology and Cognitive Science, University of Trento (Italy)
% email: ant.calcagni@gmail.com
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

function [res] = EMOT(x,y,opts)

%% Check input/default options
default_opts.thr = 0.10;
default_opts.adjLastClick = true;
default_opts.binHist = 22;
default_opts.F0iidtol = 0.01;
default_opts.verbose = true;
default_opts.maxFunEvals = 25000;
default_opts.maxIter = 25000;
default_opts.display = 'none';
default_opts.algorithm = 'interior-point';
default_opts.sa_Tmin = 14;
default_opts.sa_Tmax = 62;
if nargin==3, opts = parse_opts(default_opts,opts); elseif nargin==2, opts=default_opts; elseif nargin<2 error('At least x and y must be provided.');end

if opts.verbose, disp('@ EMOT started'); end
%% Filtering coordinates near the starting point
xraw=x; yraw=y;
y(y<=opts.thr) = NaN;x((isnan(y))) = NaN;
x(isnan(x))=[];y(isnan(y))=[];

try

%% Computing radians from xy coordinates
%%% From x-y values to polar values
k=0;
for i=1:length(x)
    if x(i) && y(i) ~= 0
        k=k+1;
        pols(k) = angleX(x(i),y(i));
    end
end

%%% Rescaled polar values between 0 and 90
rescaled_pols = pols' + repmat(360-180,length(pols),1);
rescaled_pols(rescaled_pols>=360) = rescaled_pols(rescaled_pols>=360) - 360;

%%% From polar values to radians
theta = degtorad(rescaled_pols);

% Radians of last-click movement points
lastClick = angleX(x(end),y(end)) + (360-180);
if lastClick >= 360, lastClick=lastClick-360; end
lastClick=degtorad(lastClick);

% Adjusting for the last-click point
if opts.adjLastClick, theta(find(lastClick==theta)) = []; end

%% Modeling radians with a histogram
if isa(opts.binHist,'double'), xHist = 0:(3.14/opts.binHist):3.14; 
elseif strcmp(opts.binHist,'auto'),
    binHist = sshist(theta,18:70); if mod(binHist,2)==1, binHist=binHist-1; end
    xHist = 0:(3.14/binHist):3.14; 
elseif strcmp(opts.binHist,'sa'),
    SAres = sensAnalyHist(xraw,yraw,opts.sa_Tmin,opts.sa_Tmax,false,opts.verbose); binHist=SAres.T;
    xHist = 0:(3.14/binHist):3.14;
end
H_theta = histc(theta,xHist);

%% Entropy decomposition
%%% Computing H_theta0
theta0 = builtin('_mergesimpts',theta,opts.F0iidtol); 
H_theta0 = histc(theta0,xHist);

%%% Call entropy decomposition routine
res = eDecomposition(H_theta,H_theta0,xHist,opts);

%% Save other information
res.xref = x;
res.yref = y;
res.theta = theta;
res.theta0 = theta0;
if strcmp(opts.binHist,'sa'), res.sa.T = SAres.T; res.sa.acc = SAres.acc; res.sa.data = SAres.data; end

if opts.verbose, disp('@ EMOT finished'); end

catch
    if opts.verbose, disp('@ EMOT finished: An error occurred. Trajectories must be disregarded.'); end
    res = saveFailed();res.xref = NaN; res.yref = NaN; res.theta = NaN; res.theta0 = NaN; end

end