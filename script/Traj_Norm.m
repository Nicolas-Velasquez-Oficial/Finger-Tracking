function [ normTraj, normPoints ] = Traj_Norm( trajectory, type, control, method )
%Santiago Alonso-Diaz (2016)
%
%Normalizes a single movement trajectory in space or time by
%overfitting the movement trajectory to a piecewise polynomial. In the case
%of space normalizations, the code also finds the inverse function to
%locate points in time that correspond to a given position in the
%normalizing axis and the other non-normalized axes. 
%
%
%Input
%   trajectory: nx3 matrix; rows: movement samples (in mm).
%                           columns: axis (x, y, z). 
%               trajectory must start at the origin [0,0,0],without
%               NaN.
%
%               Hint: To start at the origin, just substract the first
%               position from all the remaining trajectory points.
%               
%               Hint 2: to remove NaNs use inpaint_nans in santiagoalonso
%               github or a more fancy one inpaint_nans by John
%               D'Errico (https://www.mathworks.com/matlabcentral/fileexchange/4551-inpaint-nans)
%
%   type:       of normalization; 1 space, 2 time; 
%
%               When normalizing by space, the normalizing axis is chunked 
%               at equal forward steps (see below). This means that if 
%               there are pullbacks in the normalizing axis these would be
%               'jumped' by the algorithm.  
%               If pullbacks are too large, be aware that shape information
%               during pullback time is invisible to the space normalizing 
%               algorithm (tip: use time normalization instead).
%
%               For space  normalization, if you have a  trajectory that 
%               first goes forward (e.g. to screen) and then goes back 
%               again (e.g. to button box), break the the trajectory in two 
%               by using the max. distance in the forward direction as
%               breaking point. Then use this code to normalize either or both 
%               directions.
%
%
%   control:    vector (for time normalizing a 2D vector; for space 4D); 
%               element 1: 
%                         number of normalizing points (e.g. 100)
%               element 2: 
%                         sampling rate in Hz of the recording machine
%               element 3 (only for type 1 i.e. space normalizing) 
%                          normalizing distance in mm  (e.g. if 
%                          depth, then distance from start position to 
%                          screen). The sign is IMPORTANT e.g. if depth 
%                          normalizing and towards screen is more negative 
%                          then the  normalizing distance should be
%                          negative.
%                          
%                          Write '1' or '-1' if you want the trajectory 
%                          to be normalized in regards to the max of the 
%                          normalizing axis. In such case the normalization 
%                          can be interpreted as proportion of advancement. 
%                          '-1' will tell the algorithm that 'farther' 
%                          away is negative  
%                          '+1' to tell it that farther away is more positive.
%               element 4 (only for type 1 i.e. space normalizing) 
%                          space normalizing axis 1 for x; 2 for y; 3 for z
%
%   method:     for interpolation; string; 'nearest', 'next', 'previous', 
%               'linear','spline','pchip', or 'cubic'.
%               For most purposes, 'linear' or 'spline' work well.
%
%Output
%   normTraj:       normalized trajectory; nx2 matrix if type space (each column
%                   is a normalized axis e.g. if depth normalized, then each
%                   column are the remaining axes, horizontal and vertical).
%                   nx3 if type time (each column an axis normalized to time)
%
%   normPoints:     points at which normalization took place.

if any(trajectory(1,:))
    error('''trajectory'' does not start at origin [0,0,0]. Substract the first position from the others')
elseif any(isnan(trajectory(:,1))) 
    error('''trajectory'' has NaNs. Tip: use inpaint_nans.m')
elseif length(control)<2
    error('''control'' input is the wrong size')
end


normalizeFrames = control(1);
frameRate = control(2);
ms_sample = (1000/frameRate); %ms per sample.
startT = ms_sample; %earliest time point
increaseT = ms_sample;
timePoints = startT + (0:(size(trajectory,1)-1))*increaseT; %in ms (original)
pp_x = interp1(timePoints,trajectory(:,1),method,'pp'); %piecewise polynomial i.e. parametric form of each axis: axis(time)
pp_y = interp1(timePoints,trajectory(:,2),method,'pp');
pp_z = interp1(timePoints,trajectory(:,3),method,'pp');
pp = {pp_x,pp_y,pp_z};
switch type
    case 1 %space
        if length(control)~=4
            error('''control'' input is the wrong size')
        elseif abs(trajectory(end,control(4))) < abs(control(3))
            error('max distance traveled in normalizing axis is too short')
        elseif any(diff(trajectory(:,control(4)))<0)
            warning('there are pullbacks in the normalizing axis')
        end        
        
        dist_to_normalize = control(3);
        normalizing_axis = control(4);
        normalized_axes = 1:3; normalized_axes = normalized_axes(normalized_axes~=control(4));
        if dist_to_normalize == 1
            dist_to_normalize = max(trajectory(:,normalizing_axis));
        elseif dist_to_normalize == -1 
            dist_to_normalize = min(trajectory(:,normalizing_axis));
        end
        startT = 0; %start of normalization.
        increaseT = (dist_to_normalize-startT)/(normalizeFrames);
        normPoints = startT + (0:(normalizeFrames-1))*increaseT;
        pp_nax = pp{normalizing_axis};
        time_0 = 0; %initial value for numerical routine that finds roots (fzero)
        normtimePoints = zeros(1,size(normPoints,2));
        for i = 1:length(normPoints) %inverse procedure
            pos_i = normPoints(i); %desired interpolated value
            fun = @(time) ppval(pp_nax,time) - pos_i; %when equal to zero, this function is the inverse of the piecewise polynomial (pp_nax) i.e. time given a desired position pos_i: time(axis)
            normtimePoints(i) = fzero(fun,time_0); %finds roots of 'fun' i.e. the inverse: time(axis)
            if i~=length(normPoints) 
                time_0 = find(trajectory(:,normalizing_axis)<normPoints(i+1),1,'last')*ms_sample; %The time of the closest and latest position to the next interpolation point is the starting search time for the next fzero. This will jump any pullbacks.
            end    
        end
        
        if any(diff(normtimePoints)<0) 
            error('some of the time marks obtained in the inverse procedure go backward')
        end
        
        mse = sum((normPoints - ppval(pp_nax,normtimePoints)).^2)/normalizeFrames;
        if mse>(10^(-5))
            error('could not obtain appropriate time marks for the interpolation points')
        end
        
        normTraj = [ppval(pp{normalized_axes(1)},normtimePoints)',...
                    ppval(pp{normalized_axes(2)},normtimePoints)']; %e.g. col 1: x normalized to y; col 2: z normalized to y
             
        
    case 2 %time
        
        movement_time = size(trajectory,1)*ms_sample;
        increaseT = (movement_time-startT)/(normalizeFrames);
        normtimePoints = startT + (0:(normalizeFrames-1))*increaseT; %in ms (normalized time)
        normTraj = [ppval(pp{1},normtimePoints)', ...
                    ppval(pp{2},normtimePoints)', ...
                    ppval(pp{3},normtimePoints)']; %col 1: x normalized to time; col 2: y; col 3: z
        normPoints = normtimePoints;
                     
    otherwise
        error('invalid ''type'' input')
end


%Functional Data Analysis approach (for reference ... DO NOT ERASE)
% Based on Dr Chapman's codes in ACE lab (http://www.per.ualberta.ca/acelab/?page_id=372)
% You might need to download some functions from octave.


% data = {trajectory}; %Structure; each element is a nx3 matrix; n = optotrak samples; columns axis.
% toNormalize = length(data); %Number of trajectories
% normalizeFrames = 100; 
% normalizeType = 3; %1 = to time; 2 = to x distance; 3 = to y distance; 4 = to z distance
% frameRate = 200;
%
% normalizedReach = normalizeFDA(data,toNormalize,normalizeFrames,normalizeType,frameRate); %It uses 10*frameRate for resampling (check code to change)


end









