from gopigo import *
import time
import numpy as np

en_debug = 1

DPR = 360.0/64
WHEEL_RAD = 3.25 # Wheels are ~6.5 cm diameter. 
CHASS_WID = 13.5 # Chassis is ~13.5 cm wide.DPR = 360.0/64

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


def mapLoc(x, y, x_prime, y_prime, theta):
    a = [[np.cos(theta), -np.sin(theta), x],
                [np.sin(theta), np.cos(theta), y],
                [0, 0, 1]]

    p = np.transpose([[x_prime, y_prime, 1]])

    return np.matmul(a, p)

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

def cm2pulse(dist):
    '''
    Calculate the number of pulses to move the chassis dist cm.
    pulses = dist * [pulses/revolution]/[dist/revolution]
    '''
    wheel_circ = 2*math.pi*WHEEL_RAD # [cm/rev] cm traveled per revolution of wheel
    revs = dist/wheel_circ
    PPR = 18 # [p/rev] encoder Pulses Per wheel Revolution
    pulses = PPR*revs # [p] encoder pulses required to move dist cm.
    if en_debug:
        print 'WHEEL_RAD',WHEEL_RAD
        print 'revs',revs
        print 'pulses',pulses
    return pulses

def fwd_cm(dist=None):
    if dist is not None:
        pulse = int(cm2pulse(dist))
        enc_tgt(1,1,pulse)
    fwd()

def move(x, theta):
    left_deg(theta)

    fwd_cm(x)

if __name__ == '__main__':
    servo(90)
    set_speed(100)

    while not detect(20):
            fwd_cm(3)

    left_deg(90)
    servo(0)
    while True:
        while detect(20):
            fwd_cm(3)
            
        theta = 10
        count = 0

        while not detect(20):
            right_deg(theta)
            count += 1

        fwd_cm(3)

    # move(10, 30)
    # print(mapLoc(0, 0, 10, 0, 30))






