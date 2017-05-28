from gopigo import *
import time

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
                
                

    print(angles[-1] - angles[0])

        
