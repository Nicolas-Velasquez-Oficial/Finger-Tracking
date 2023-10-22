import math

def angleX(x, y):
    deg = -((math.atan2(y, x)) * 360) / (2 * math.pi)
    if deg > 0 and deg < 180:
        p = deg
    elif deg == -180:
        p = deg * -1
    elif deg == 0.0:
        p = 360.00
    elif deg < 0.0 and deg > -180:
        p = 360.00 - (deg * -1)
    return p