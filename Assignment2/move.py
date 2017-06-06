from gopigo import *
import numpy as np
import time

DPR = 360.0/64
WHEEL_RAD = 3.25 # Wheels are ~6.5 cm diameter. 
en_debug=1

X = 0
Y = 0
theta = 0
Original_Pos = [[0],[0],[1]]
Previous_Matrix = [[1, 0, 0],
                   [0, 1, 0],
                   [0, 0, 1]]

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
    

def transform_matrix(rotate_angle, x_move, y_move):
    T = [[np.cos(rotate_angle/180.*3.14), -np.sin(rotate_angle/180.*3.14), x_move],
         [np.sin(rotate_angle/180.*3.14),  np.cos(rotate_angle/180.*3.14), y_move],
         [              0               ,                  0             ,   1   ]]
    return T


def update_pos(theta_change, X_change, Y_change):
    global X
    global Y
    global theta
    global Previous_Matrix
    Previous_Matrix = np.dot(Previous_Matrix,transform_matrix(theta_change,X_change,Y_change))
    Current_Pos = np.dot(Previous_Matrix,Original_Pos)
    X = Current_Pos[0]
    Y = Current_Pos[1]
    theta += theta_change
    if theta > 180:
        theta -= 360
    if theta < -180:
        theta += 360
    if en_debug:
        print "theta", theta
        print "X", X
        print "Y", Y

def distance(x,y,k):
    return abs(y-k*x)/np.sqrt(1+k**2)

def On_mline(x_goal, y_goal, x, y):
    #y=kx
    error = 3
    if(x_goal==0): #k not exist
        if(x<=error):
            return True
        else:
            return False

    k = y_goal/x_goal
    dist = distance(x,y,k)
    if(dist<=error):
        print "In the line"
        return True
    else:
        print "Out the line"
        return False

if __name__ == '__main__':
    x_goal = 0
    y_goal = 10
    
    X_change = 0
    Y_change = 0
    theta_change = 0
    set_speed(100)

    #Test 1
    #Run a triangle to test
    #It will run back to start point
##    theta_change = 30
##    left_deg(theta_change)
##    update_pos(theta_change,0,0)
##    time.sleep(5)
##    
##    X_change = 50
##    fwd_cm(X_change)
##    update_pos(0,X_change,0)
##    time.sleep(10)
##    
##    theta_change = 120
##    left_deg(theta_change)
##    update_pos(theta_change,0,0)
##    time.sleep(5)
##    
##    fwd_cm(X_change)
##    update_pos(0,X_change,0)
##    time.sleep(10)
##
##    left_deg(theta_change)
##    update_pos(theta_change,0,0)
##    time.sleep(5)
##    
##    fwd_cm(X_change)
##    update_pos(0,X_change,0)
##    time.sleep(10)

    #Test 2
    #Keep turning
    #It is finally reach 60 degrees
    for i in range(18):
        print(i)
        theta_change = 20
        left_deg(26)
        time.sleep(3)
        update_pos(theta_change,0,0)

    #Test 3
##    X_change = 1
##    Y_change = 1
##    while True:
##        update_pos(0,0,Y_change)
##        update_pos(0,X_change,0)
##        if On_mline(x_goal, y_goal, X, Y) == False:
##            break
##        time.sleep(1)
        
##    update_pos(0,X_change,0)
##    On_mline(x_goal, y_goal, X, Y)
##    update_pos(0,X_change,0)
##    On_mline(x_goal, y_goal, X, Y)
##    update_pos(0,X_change,0)
##    On_mline(x_goal, y_goal, X, Y)
    


