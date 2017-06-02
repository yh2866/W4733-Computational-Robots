from gopigo import *
import time

#The real 20cm correspond to 25cm in sensor
STOP_DIST = 25

######Move forward##########
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
    print "Found obstacle"
    return

######Move backward##########
def move_backward(min_dist):
    ## Set servo to point straight ahead
    servo(90)
    set_speed(200)
    print "Moving Forward"

    while detect(STOP_DIST):
        motor_bwd()
        time.sleep(0.1)
        stop()
    
    time.sleep(3)
    print "Found obstacle"
    return

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

#############Main Function################
if __name__ == "__main__":
    objectDetected = False
    count = 0
    servo(90)
    time.sleep(0.1)
    angles = []
    set_speed(200)
    #Detect Objects 
    while not objectDetected:
        left_rot()
        time.sleep(0.04)
        stop()
        #The real 100cm correspond to 130cm in sensor
        objectDetected = detect(130)  
    #When object was detected, calculate the count
    while objectDetected:
        count += 1
        left_rot()
        time.sleep(0.04)
        stop()
        #The real 100cm correspond to 130cm in sensor
        objectDetected = detect(100)  

    time.sleep(0.1)
    print(count)

    #Turn back with half of accounted numbers
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
    
    #Move forward or backward according to the distance
    if detect(STOP_DIST):
        move_backward(STOP_DIST)
    else:
        move_forward(STOP_DIST)                                

