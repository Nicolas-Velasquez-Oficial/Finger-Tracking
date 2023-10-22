def parse_opts(default_opts, opts):
    if not 'thr' in opts:
        opts['thr'] = default_opts['thr']
    if not 'adjLastClick' in opts:
        opts['adjLastClick'] = default_opts['adjLastClick']
    if not 'F0iidtol' in opts:
        opts['F0iidtol'] = default_opts['F0iidtol']
    if not 'maxFunEvals' in opts:
        opts['maxFunEvals'] = default_opts['maxFunEvals']
    if not 'maxIter' in opts:
        opts['maxIter'] = default_opts['maxIter']
    if not 'display' in opts:
        opts['display'] = default_opts['display']
    if not 'algorithm' in opts:
        opts['algorithm'] = default_opts['algorithm']
    if not 'verbose' in opts:
        opts['verbose'] = default_opts['verbose']
    if not 'binHist' in opts:
        opts['binHist'] = default_opts['binHist']
    if not 'sa_Tmin' in opts:
        opts['sa_Tmin'] = default_opts['sa_Tmin']
    if not 'sa_Tmax' in opts:
        opts['sa_Tmax'] = default_opts['sa_Tmax']
    return opts