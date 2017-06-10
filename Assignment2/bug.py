from gopigo import *
import time
import numpy as np
import matplotlib.pyplot as plt

en_debug = 1

DPR = 360.0/64
WHEEL_RAD = 3.25 # Wheels are ~6.5 cm diameter.
CHASS_WID = 13.5 # Chassis is ~13.5 cm wide.DPR = 360.0/64

X = 0.0
Y = 0.0
X_Goal = 100.0
Y_Goal = 100.0
theta = 0
ERROR_mline = 3
ERROR_goal = 3
Plot_X = []
Plot_Y = []
OBSTACLE_X = []
OBSTACLE_Y = []
Original_Pos = [[0],[0],[1]]
Previous_Matrix = [[1, 0, 0],
                   [0, 1, 0],
                   [0, 0, 1]]

MLINE_X = []
MLINE_Y = []

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
    SAMPLE = 6
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
    Plot_X.append(X)
    Plot_Y.append(Y)
    if en_debug:
        print "theta", theta
        print "X", X
        print "Y", Y


def isGoal(X_Goal, Y_Goal, X, Y):
    return abs(X - X_Goal) <= ERROR_goal and abs(Y - Y_Goal) <= ERROR_goal



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

    if(x_goal==0): #k not exist
        if(x<=ERROR_mline):
            return True
        else:
            return False

    k = y_goal/x_goal
    dist = distance(x,y,k)
    if(dist<=ERROR_mline):
        return True
    else:
        return False

def avoidObjectOnLeft():
    obstacle_move = 0
    right_deg(110)
    time.sleep(1)
    update_pos(-90,0,0)
    time.sleep(0.5)
    scale = 1.2

    onGoal = False
    onMLine = False

    while True:
        servo(180)

        while True:

            # move forward
            while detect(20) and not detect(5):
                servo(90)

                if not detect(20):
                    OBSTACLE_X.append(X)
                    OBSTACLE_Y.append(Y + 20)
                    fwd_cm(3)
                    obstacle_move += 3
                    onGoal, onMLine = posFeedback(0, 3, 0)

                else:
                    OBSTACLE_X.append(X - 20)
                    OBSTACLE_Y.append(Y)
                    right_deg(90)
                    update_pos(-90,0,0)
                    time.sleep(1)

                servo(180)

                if onGoal:
                    return
                elif onMLine and obstacle_move>10: #
                    final_angle = np.arctan((Y_Goal/ X_Goal)) / 3.14 * 180
                    rot_angle = final_angle - theta
                    if rot_angle < 0:
                        right_deg(abs(rot_angle)*scale)
                        update_pos(-abs(rot_angle), 0, 0)
                    else:
                        left_deg(abs(rot_angle)*scale)
                        update_pos(abs(rot_angle), 0, 0)

                    servo(90)
                    print("On M Line !!! ")
                    print("On M Line !!! ")
                    print("On M Line !!! ")

                    if(bug2()):
                        return

            servo(180)

            if not detect(20):
                break
            else:
                right_deg(22)
                update_pos(-20, 0, 0)

        theta_change = 20
        theta_actual_change = 26

        # for rotation to avoid object
        while not detect(20):
            servo(90)

            if not detect(20):
                print("not detect")
                time.sleep(0.5)
                left_deg(theta_actual_change)
                time.sleep(1)
                update_pos(theta_change,0,0)
                time.sleep(1)
            else:
                print("detect")
                right_deg(60)
                update_pos(-60,0,0)
                time.sleep(0.5)
            servo(0)

def avoidObjectOnRight():
    obstacle_move = 0
    left_deg(110)
    time.sleep(1)
    update_pos(90,0,0)
    time.sleep(0.5)
    scale = 1.2

    onGoal = False
    onMLine = False

    while True:
        servo(0)

        while True:
            # move forward
            while detect(20) and not detect(10):
                servo(90)

                if not detect(20):
                    OBSTACLE_X.append(X)
                    OBSTACLE_Y.append(Y - 20)
                    fwd_cm(3)
                    obstacle_move += 3
                    onGoal, onMLine = posFeedback(0, 3, 0)

                else:
                    OBSTACLE_X.append(X + 20)
                    OBSTACLE_Y.append(Y)
                    left_deg(90)
                    update_pos(90,0,0)
                    time.sleep(1)

                servo(0)

                if onGoal:
                    return
                elif onMLine and obstacle_move>10:
                    if len(MLINE_X) == 0 or \
                       (len(MLINE_X) > 0 and (X ** 2 + Y ** 2) < (MLINE_X[-1]**2 + MLINE_Y[-1]**2)):
                        MLINE_X.append(X)
                        MLINE_Y.append(Y)

                   final_angle = np.arctan((Y_Goal/ X_Goal)) / 3.14 * 180
                   print "final_angle ", final_angle

                    rot_angle = final_angle - theta

                    if rot_angle < 0:
                        right_deg(abs(rot_angle)*scale)
                        update_pos(-abs(rot_angle), 0, 0)
                    else:
                        left_deg(abs(rot_angle)*scale)
                        update_pos(abs(rot_angle), 0, 0)

                    servo(90)
                    print("On M Line !!! ")
                    print("On M Line !!! ")
                    print("On M Line !!! ")



                    if(bug2()):
                        return

            servo(0)

            if not detect(20):
                break
            else:
                left_deg(22)
                update_pos(20, 0, 0)

        theta_change = 20
        theta_actual_change = 26

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

def plot_path():
    print 'Plot_x', Plot_X
    print 'Plot_y', Plot_Y
    plt.plot(Plot_X[0], Plot_Y[0], 'go')
    plt.plot(Plot_X[1:-2],Plot_Y[1:-2],'bo')
    plt.plot(Plot_X[-1], Plot_Y[-1], 'ro')
    plt.plot(Plot_X,Plot_Y,'b')
    plt.plot(OBSTACLE_X, OBSTACLE_Y, 'rx')
    plt.xlim((-20, max(X_Goal, Y_Goal) + 20 ))
    plt.ylim((-20, max(X_Goal, Y_Goal) + 20 ))


def bug2():
    onGoal = False
    onMLine = False

    servo(90)
    set_speed(100)
    scale = 1.2


    if isGoal(X_Goal, Y_Goal, X, Y):
        plot_path()
        return True
    else:
        while not detect(20):
            fwd_cm(3)
            onGoal, onMLine = posFeedback(0, 3, 0)

            if onGoal:
                plot_path()
                return True

    # now we've detected an object
    if onMLine and len(MLINE_X) > 0 \
       and abs(MLINE_X[-1] - X) <= ERROR_mline and abs(MLINE_Y[-1] - Y) <= ERROR_mline:
        avoidObjectOnLeft()
    else:
        avoidObjectOnRight()





if __name__ == '__main__':
    if X_Goal != 0 and Y_Goal > 0:
        print '(Y_Goal/ X_Goal) / 3.14 * 180',np.arctan((Y_Goal/ X_Goal) / 3.14 * 180)
        left_angle = np.arctan((Y_Goal/ X_Goal)) / 3.14 * 180
        left_deg(left_angle*scale)
        print 'left_angle', left_angle
        update_pos(left_angle,0,0)
    elif X_Goal != 0 and Y_Goal < 0:
        right_angle = np.arctan(-(Y_Goal/ X_Goal)) / 3.14 * 180
        right_deg(right_angle)
        update_pos(-right_angle,0,0)
    elif X_Goal == 0 and Y_Goal < 0:
        right_deg(90)
        update_pos(-90,0,0)
    elif X_Goal == 0 and Y_Goal > 0:
        left_deg(90)
        update_pos(90,0,0)

    bug2()
    plt.savefig("result.png")
