function [p] = angleX(x,y)

deg = -((atan2(y,x))*360)/((pi)*2); 
if deg > 0 && deg < 180
    p = deg;
elseif deg == -180 
    p = deg*-1;
elseif deg == 0.0 
    p = 360.00;   
elseif deg < 0.0 && deg > -180 
    p = 360.00-(deg*-1);        
end

end