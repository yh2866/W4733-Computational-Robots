from gopigo import *
import time

STOP_DIST = 25


def move_forward(min_dist):
    ## Set servo to point straight ahead
    servo(90)
    set_speed(200)
    #print "Moving Forward"

    while not detect(STOP_DIST):
        motor_fwd()
        time.sleep(0.1)
        stop()
    
    time.sleep(3)
    #print "Found obstacle"
    return

def move_backward(min_dist):
    ## Set servo to point straight ahead
    servo(90)
    set_speed(200)
    #print "Moving Forward"

    while detect(STOP_DIST):
        motor_bwd()
        time.sleep(0.1)
        stop()
    
    time.sleep(3)
    #print "Found obstacle"
    return

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


if __name__ == "__main__":
    objectDetected = False
    count = 0
    
    servo(90)
    time.sleep(0.1)
    angles = []
    set_speed(200)
    
    while not objectDetected:
        left_rot()
        time.sleep(0.04)
        stop()

        objectDetected = detect(100)
        

    while objectDetected:
        count += 1
        left_rot()
        time.sleep(0.04)
        stop()
        objectDetected = detect(100)

    time.sleep(0.1)
    #print(count)

    for i in range(count // 2):
        time.sleep(0.5)
        right_rot()
        time.sleep(0.04)
        stop()

    if (count % 2 == 1):
        time.sleep(0.1)
        right_rot()
        time.sleep(0.02)
        stop()
    
        
    if detect(STOP_DIST):
        move_backward(STOP_DIST)
    else:
        move_forward(STOP_DIST)                                

