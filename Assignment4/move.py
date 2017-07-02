from gopigo import *
import time

area_original = 0
original_flag = 1

## 360 roation is ~64 encoder pulses or 5 deg/pulse
## DPR is the Deg:Pulse Ratio or the # of degrees per
##  encoder pulse.
DPR = 360.0/64
WHEEL_RAD = 3.25 # Wheels are ~6.5 cm diameter. 
CHASS_WID = 13.5 # Chassis is ~13.5 cm wide.

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

def fwd_cm(dist=None):
    '''
    Move chassis fwd by a specified number of cm.
    This function sets the encoder to the correct number
     of pulses and then invokes fwd().
    '''
    if dist is not None:
        pulse = int(cm2pulse(dist))
        enc_tgt(1,1,pulse)
    fwd()

def bwd_cm(dist=None):
    '''
    Move chassis bwd by a specified number of cm.
    This function sets the encoder to the correct number
     of pulses and then invokes bwd().
    '''
    if dist is not None:
        pulse = int(cm2pulse(dist))
        enc_tgt(1,1,pulse)
    bwd()

def cm2pulse(dist):
    '''
    Calculate the number of pulses to move the chassis dist cm.
    pulses = dist * [pulses/revolution]/[dist/revolution]
    '''
    wheel_circ = 2*math.pi*WHEEL_RAD # [cm/rev] cm traveled per revolution of wheel
    revs = dist/wheel_circ
    PPR = 18 # [p/rev] encoder Pulses Per wheel Revolution
    pulses = PPR*revs # [p] encoder pulses required to move dist cm.
    return pulses

def move(cx, area_current):
    set_speed(90)
    global area_original
    global original_flag
    resolution_middle = 160
    if cx < 160-10:
        left_deg((160-cx)/2.5)
        print 'turn left', (160-cx)/2.5
        time.sleep(0.2)
    elif cx > 160+10:
        right_deg((cx-160)/2.5)
        print 'turn right', (cx-160)/2.5
        time.sleep(0.2)
    #Set the orginal area
    if original_flag == 1:
        area_original = area_current
        original_flag = 0
    #Turn the flag to 0 when original is set
    if original_flag == 0:
        if area_current/area_original<0.8:
            fwd_cm(10)
            time.sleep(0.2)
        elif area_current/area_original>1.2:
            bwd_cm(10)
            time.sleep(0.2)






