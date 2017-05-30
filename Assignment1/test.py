from gopigo import *
import time

if __name__ == "__main__":
 	servo(90)
   	time.sleep(1)
        dis = us_dist(15)

        set_speed(100)
 	left_rot()

 	while True:
            i = us_dist(15)
            time.sleep(0.2)
            print(i)
