from gopigo import *
import time
import numpy as np
#from scipy.optimize import fsolve

SAMPLE = 10
REQUIRED = 8


#def calculate_angle(alpha, d):
#    m = 0
#    e = 0
#    l = d*np.tan(alpha/2)
#
#    return [m+e-l, -np.sin(np.arctan(m/d)) - ((e**2+m**2-l**2)/(2*e*np.sqrt(m**2+d**2)))]

def calculate_angle(alpha, d):
   m = 31.5/2
   theta = np.arctan(m/d)/3.14*180.
   print ("object_angle",2.*theta)
   return alpha - 2.*theta


if __name__ == "__main__":
    angles = []

    servo(90)
    time.sleep(1)

    set_speed(60)
    time.sleep(1)

    mini_dis= 100
    
    for i in range(20, 160, 2):
        sampling = []
        servo(i)
        time.sleep(0.3)
        print("angle ", i)
        
        for j in range(SAMPLE):
                time.sleep(0.01)
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
    print ("alpha",angles[-1] - angles[0])
    #d = us_dist(15)
    print ("mini_dis",mini_dis)
    mini_dis = 30
    print ("result",calculate_angle(alpha, mini_dis))
