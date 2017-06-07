from gopigo import *
import time
import numpy as np

en_debug = 1

DPR = 360.0/64
WHEEL_RAD = 3.25 # Wheels are ~6.5 cm diameter.
CHASS_WID = 13.5 # Chassis is ~13.5 cm wide.DPR = 360.0/64

X = 0.0
Y = 0.0
X_Goal = 100.0
Y_Goal = 0.0
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


##def mapLoc(x, y, x_prime, y_prime, theta):
##    a = [[np.cos(theta/180.*3.14), -np.sin(theta/180.*3.14), x],
##                [np.sin(theta/180.*3.14), np.cos(theta/180.*3.14), y],
##                [0, 0, 1]]
##
##    p = np.transpose([[x_prime, y_prime, 1]])
##
##    r = np.matmul(a, p)
##
##    x = r[0][0]
##    y = r[0][1]
##
##    return x, y

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


def isGoal(X_Goal, Y_Goal, X, Y):
    return abs(X - X_Goal) <= 5 and abs(Y - Y_Goal) <= 5



def posFeedback(theta_change, X_change, Y_change):
    onGoal = False
    onMLine = False

    update_pos(theta_change, X_change, Y_change)
    time.sleep(0.5)

    if isGoal(X_Goal, Y_Goal, X, Y):
        onGoal = True

    if on_Mline(X_Goal, Y_Goal, X, Y):
        onMLine = True

    return onGoal, onMLine



def distance(x,y,k):
    return abs(y-k*x)/np.sqrt(1+k**2)


def on_Mline(x_goal, y_goal, x, y):
    #y=kx
    error = 5
    if(x_goal==0): #k not exist
        if(x<=error):
            return True
        else:
            return False

    k = y_goal/x_goal
    dist = distance(x,y,k)
    if(dist<=error):
        return True
    else:
        return False


def avoidObject():
    obstacle_move = 0
    left_deg(110)
    time.sleep(1)
    update_pos(90,0,0)
    time.sleep(0.5)

    while True:
        servo(0)

        # move forward
        while detect(20) and not detect(10):
            servo(90)

            if not detect(20):
                fwd_cm(3)
                obstacle_move += 3
                onGoal, onMLine = posFeedback(0, 3, 0)
                
            else:
                left_deg(90)
                update_pos(90,0,0)
                time.sleep(1)

            servo(0)

            if onGoal:
                return
            elif onMLine and obstacle_move>10:
                if theta < 0:
                    left_deg(abs(theta))
                else:
                    right_deg(theta)

                update_pos(-theta, 0, 0)
                    
                servo(90)
                print("On M Line !!! ")
                print("On M Line !!! ")
                print("On M Line !!! ")
                if(bug2()):
                    return

        theta_change = 20
        theta_actual_change = 26
        count = 0

        # for rotation to avoid object
        while not detect(20):
            servo(90)

            if not detect(20):
                print("not detect")
                time.sleep(0.5)
                right_deg(theta_actual_change)
                time.sleep(1)
                update_pos(-theta_change,0,0)
                time.sleep(1)
            else:
                print("detect")
                left_deg(60)
                update_pos(60,0,0)
                time.sleep(0.5)
            servo(0)

def bug2():
    servo(90)
    set_speed(100)

    if isGoal(X_Goal, Y_Goal, X, Y):
        return True
    else:
        while not detect(20):
            fwd_cm(3)
            onGoal, onMLine = posFeedback(0, 3, 0)

            if onGoal:
                return True

    # now we've detected an object

    avoidObject()



    # avoid object




if __name__ == '__main__':
    bug2()
