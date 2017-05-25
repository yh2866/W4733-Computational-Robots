from gopigo import *
import time

if __name__ == "__main__":
	servo(90)
 	time.sleep(1)

	while us_dist(15)>100:
		right_rot()
