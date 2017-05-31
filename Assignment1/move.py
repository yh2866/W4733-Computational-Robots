from gopigo import *
import time

STOP_DIST = 25


def move(min_dist):
    ## Set servo to point straight ahead
    servo(90)
    set_speed(200)
    print "Moving Forward"
    while us_dist(15) > min_dist:
        time.sleep(1)
        fwd()
        time.sleep(0.005)
    stop()
    time.sleep(3)
    print "Found obstacle"
    return

if __name__ == '__main__':
    move(STOP_DIST)
