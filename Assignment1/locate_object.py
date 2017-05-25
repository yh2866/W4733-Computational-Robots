from gopigo import *
import time

if __name__ == "__main__":
	servo(90)
 	time.sleep(1)

 	set_speed(60)
 	time.sleep(1)

 	#right_rot()

	while True:
		print us_dist(15)
		right_rot()

		if us_dist(15) <= 100:
			stop()
			break


