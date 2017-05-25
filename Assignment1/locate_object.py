from gopigo import *
import time

if __name__ == "__main__":
	servo(90)
 	time.sleep(1)

 	if us_dist(15) < 100:
 		continue
 	else:
		while us_dist(15)>100:
			print us_dist(15)
			right_rot()
		stop()

	
