from gopigo import *
import time
import numpy as np
from scipy.optimize import fsolve

SAMPLE = 10
REQUIRED = 8

#Test 1
Width1 = 31.5
Distance1 = 43.5
Angle1 = atan(32.5/2,43.5)*2.0

if __name__ == "__main__":
    angles = []

    servo(90)
    time.sleep(1)

    set_speed(60)
    time.sleep(1)

    for i in range(0, 180, 5):
        sampling = []
        servo(i)
        time.sleep(0.3)
        print("angle ", i)
        
        for j in range(SAMPLE):
                time.sleep(0.05)
                d = us_dist(15)
                
                print(d)
                
                if d <= 100 and d > 0:
                        sampling.append(d)

        if len(sampling) >= REQUIRED:
                angles.append(i)

    #########################
    """
    calculate theta as the final result
    """
    alpha = angles[-1] - angles[0]
    d = us_dist(15)
    m, e = fsolve(calculate_angle(), [alpha, d])
    theta0 = np.arctan(m/d)
    theta = (alpha - theta0*2)  
    #########################

    print(angles[-1] - angles[0])

        
def calculate_angle(alpha, d):
    m = 0
    e = 0
    l = d*tan(alpha/2)

    return [m+e-l, -np.sin(np.arctan(m/d)) - ((e**2+m**2-l**2)/(2*e*np.sqrt(m**2+d**2)))]