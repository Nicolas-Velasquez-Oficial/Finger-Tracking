function [opts] = parse_opts(default_opts,opts)
opts=opts;

if ~isfield(opts,'thr'), opts.thr = default_opts.thr;end
if ~isfield(opts,'adjLastClick'), opts.adjLastClick = default_opts.adjLastClick;end
if ~isfield(opts,'F0iidtol'), opts.F0iidtol = default_opts.F0iidtol;end
if ~isfield(opts,'maxFunEvals'), opts.maxFunEvals = default_opts.maxFunEvals;end
if ~isfield(opts,'maxIter'), opts.maxIter = default_opts.maxIter;end
if ~isfield(opts,'display'), opts.display = default_opts.display;end
if ~isfield(opts,'algorithm'), opts.algorithm = default_opts.algorithm;end
if ~isfield(opts,'verbose'), opts.verbose = default_opts.verbose;end
if ~isfield(opts,'binHist'), opts.binHist = default_opts.binHist;end
if ~isfield(opts,'sa_Tmin'), opts.sa_Tmin = default_opts.sa_Tmin;end
if ~isfield(opts,'sa_Tmax'), opts.sa_Tmax = default_opts.sa_Tmax;end

end


