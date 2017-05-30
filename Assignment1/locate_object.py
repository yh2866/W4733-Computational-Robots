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
    angle = 0
    servo(0)
    DPR = 360.0/64

    inc = 4
    for ang in range(1,179,inc):
        sampling = []
        time.sleep(0.05)
        #print("angle ", i)
        
        for j in range(SAMPLE):
                time.sleep(0.01)
                d = us_dist(15)
                
                #print(d)
                
                if d <= 100 and d > 0:
                        sampling.append(d)

        if len(sampling) >= REQUIRED:
                objectDetected = True
                angle = i
                break   
        if objectDetected:
            angle = ang
            #objectDetected, angle = scanOneEighty()
            break
        servo(ang)
        #left_deg(inc)
    # if no object detected within 180 degrees
    if objectDetected == False:
        left_deg(180)
        servo(0)
        for ang in range(1,179,inc):
            sampling = []
            time.sleep(0.05)
            print("angle ", i)
            
            for j in range(SAMPLE):
                    time.sleep(0.05)
                    d = us_dist(15)
                    
                    print(d)
                    
                    if d <= 100 and d > 0:
                            sampling.append(d)

            if len(sampling) >= REQUIRED:
                    objectDetected = True
                    angle = i
                    break   
            if objectDetected:
                angle = ang
                #objectDetected, angle = scanOneEighty()
                break
            servo(ang)
            

    servo(90)
    #set_speed(50)
    turn_to(angle)
    move(STOP_DIST)                                

