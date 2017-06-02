from gopigo import *
import time
import numpy as np

DPR = 360.0/64

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


def mapLoc(x y, x_prime, y_prime, theta):
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

def fwd_cm(dist=None):
    ’’’
    Move chassis fwd by a specified number of cm.
    This function sets the encoder to the correct number
     of pulses and then invokes fwd().
    ’’’
    if dist is not None:
        pulse = int(cm2pulse(dist))
        enc_tgt(1,1,pulse)
    fwd()

def move(x, theta):
    left_deg(theta)

    fwd_cm(x)

if __name__ == '__main__':
    # servo(0)


    # while True:
    #     d = us_dist(15)

    move(10, 30)
    print(mapLoc(0, 0, 10, 0, 30))






