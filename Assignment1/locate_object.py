from gopigo import *
import time

if __name__ == "__main__":
	servo(90)
 	time.sleep(1)

 	set_speed(10)
 	time.sleep(1)
 	
	while us_dist(15)>100:
		print us_dist(15)
		right_rot()
	stop()


