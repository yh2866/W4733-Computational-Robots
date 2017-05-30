from gopigo import *
import time

SAMPLE = 10
REQUIRED = 7
STOP_DIST = 20

def left_deg(deg=None):
    '''
    Turn chassis left by a specified number of degrees.
    DPR is the #deg/pulse (Deg:Pulse ratio)
    This function sets the encoder to the correct number
     of pulses and then invokes left().
    '''
    if deg is not None:
        pulse= int(deg/DPR)
        enc_tgt(0,1,pulse)
    left()

def right_deg(deg=None):
    '''
    Turn chassis right by a specified number of degrees.
    DPR is the #deg/pulse (Deg:Pulse ratio)
    This function sets the encoder to the correct number
     of pulses and then invokes right().
    '''
    if deg is not None:
        pulse= int(deg/DPR)
        enc_tgt(1,0,pulse)
    right()

def move(min_dist):
    ## Set servo to point straight ahead
    servo(90)
    print "Moving Forward"
    while us_dist(15) > min_dist:
        fwd()
        time.sleep(0.04)
    stop()
    time.sleep(3)
    print "Found obstacle"
    return		

def turn_to(angle):
    '''
    Turn the GoPiGo to a specified angle where angle=0 is 90deg 
    the way to the right and angle=180 is 90deg to the left.
    The GoPiGo is currently pointing forward at angle==90.
    '''
    ## <0 is turn left, >0 is turn right.
    degs = angle-90
    print "Turning craft {} degrees".format(degs),
    if degs > 0:
        print "to the left"
        if degs < 10:
            degs = 10
        left_deg(degs)
    else:
        print "to the right"
        if degs > -10:
            degs = -10
        right_deg(-1 * degs)
    ## This sleep is really just for debugging so I can verify that it turned properly
    time.sleep(1)

    


if __name__ == "__main__":
    objectDetected = False
    scanFinished = False
    angle = 1
    servo(1)
    DPR = 360.0/64
    angles = []
    inc = 4
    #scan the 180 degrees range in front
    for ang in range(1,177,inc):
        servo(ang)
        sampling = []
        time.sleep(0.05)

        for j in range(SAMPLE):
                time.sleep(0.001)
                d = us_dist(15)             
                if d <= 50 and d > 0:
                        sampling.append(d)
        #if object detected
        if len(sampling) >= REQUIRED:
            objectDetected = True
            angles.append(ang)
        if objectDetected:
            angles.append(ang)
            if d >50:
                scanFinished = True
        if scanFinished:
            angle = (angles[-1]+angles[0])/2
            break
        if ang == 177 and scanFinished == False:  #keep finding the obstacle until right 
            angle = ang+30
            break
        if objectDetected == True and ang<20:
            angle = 0
            break

    # if no object detected within 180 degrees, turn 180 degrees and scan again
    if objectDetected == False:
        left_deg(180)
        servo(0)
        for ang in range(1,179,inc):
            servo(ang)
            sampling = []
            time.sleep(0.05)

            for j in range(SAMPLE):
                    time.sleep(0.001)
                    d = us_dist(15)             
                    if d <= 50 and d > 0:
                            sampling.append(d)
            #if object detected
            if len(sampling) >= REQUIRED:
                objectDetected = True
                angles.append(ang)
            if objectDetected:
                angles.append(ang)
                if d >50:
                    scanFinished = True
            if scanFinished:
                angle = (angles[-1]+angles[0])/2
                break
            if ang == 177 and scanFinished == False:  #keep finding the obstacle until right 
                angle = ang+30
                break
            if objectDetected == True and ang<20:
                angle = 0
                break          

    servo(90)
    print "The car is facing towards %s degrees"%angle
    turn_to(angle)
    move(STOP_DIST)                                

