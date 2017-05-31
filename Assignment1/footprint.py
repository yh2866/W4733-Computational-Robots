from gopigo import *
import time
import numpy as np

SAMPLE = 10
REQUIRED = 8


def calculate_angle(alpha, d):
   m = 31.5/2
   theta = np.arctan(m/d)/3.14*180.
   print ("object_angle",2.*theta)
   return alpha - 2.*theta

def methodOne():
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
   mini_dis = 30
   print ("result",calculate_angle(alpha, mini_dis))

#####Detect the object#######
def detect(dist):
    SAMPLE = 5
    REQUIRED = 3
    
    sampling = []
    for j in range(SAMPLE):
        time.sleep(0.07)
        
        d = us_dist(15)
        print(d)
        if d <= dist and d > 0:
            sampling.append(d)

    if len(sampling) >= REQUIRED:
        return True
    else:
        return False


def methodTwo():
   servo(90)
   time.sleep(0.1)

   angles = []
   dist = 100

   for j in range(90, 180, 2):
      servo(j)
      if detect(dist):
         angles.append(j)
   print("start ", angles[0])
   print("end ", angles[-1])
   return (angles[-1] - angles[0]) * 2


if __name__ == "__main__":
    # methodOne()
    print(methodTwo())
