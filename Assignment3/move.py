from gopigo import *
import time
import numpy as np
import matplotlib.pyplot as plt
import sys

en_debug = 1

DPR = 360.0/64
WHEEL_RAD = 3.25 # Wheels are ~6.5 cm diameter.
CHASS_WID = 13.5 # Chassis is ~13.5 cm wide.DPR = 360.0/64

X = 0.0
Y = 0.0
X_GOAL = 100.0
Y_GOAL = 100.0
theta = 0

ERROR_goal = 6


PLOT_X_LIST = []
PLOT_Y_LIST = []
OBSTACLE_X_LIST = []
OBSTACLE_Y_LIST = []
Original_Pos = [[0],[0],[1]]
Previous_Matrix = [[1, 0, 0],
                   [0, 1, 0],
                   [0, 0, 1]]

HIT_MLINE_X_LIST = []
HIT_MLINE_Y_LIST = []

LEAVE_MLINE_X_LIST = []
LEAVE_MLINE_Y_LIST = []
SECONDVISITMLINE = -1

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


def detect(d1, d2):
    SAMPLE = 5
    REQUIRED = 2

    sampling = []
    for j in range(SAMPLE):
        time.sleep(0.07)

        d = us_dist(15)
        # print(d)
        if d <= d1 and d > d2:
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
    global OBSTACLE_X
    global OBSTACLE_Y

    Currrent_Pos_Temp = np.dot(Previous_Matrix, transform_matrix(-90,0,0))
    Currrent_Pos_Temp = np.dot(Currrent_Pos_Temp, transform_matrix( 0 ,10,0))
    Currrent_Pos_Obstacle = np.dot(Currrent_Pos_Temp, Original_Pos)

    Previous_Matrix = np.dot(Previous_Matrix,transform_matrix(theta_change,X_change,Y_change))
    Current_Pos = np.dot(Previous_Matrix,Original_Pos)

    X = Current_Pos[0]
    Y = Current_Pos[1]

    theta += theta_change
    if theta > 180:
        theta -= 360
    if theta < -180:
        theta += 360
    PLOT_X_LIST.append(X)
    PLOT_Y_LIST.append(Y)
    if en_debug:
        print "theta", theta
        print "X", X
        print "Y", Y


# def isGoal(X_GOAL, Y_GOAL, X, Y):
#     return abs(X - X_GOAL) <= ERROR_goal and abs(Y - Y_GOAL) <= ERROR_goal

# def orient_to_goal():
#     scale = 1.2
#     if X_GOAL != 0 and Y_GOAL > 0:
#         print '(Y_GOAL/ X_GOAL) / 3.14 * 180',np.arctan((Y_GOAL/ X_GOAL) / 3.14 * 180)
#         left_angle = np.arctan((Y_GOAL/ X_GOAL)) / 3.14 * 180
#         left_deg(left_angle*scale)
#         print 'left_angle', left_angle
#         update_pos(left_angle,0,0)
#     elif X_GOAL != 0 and Y_GOAL < 0:
#         right_angle = np.arctan(-(Y_GOAL/ X_GOAL)) / 3.14 * 180
#         right_deg(right_angle)
#         update_pos(-right_angle,0,0)
#     elif X_GOAL == 0 and Y_GOAL < 0:
#         right_deg(90)
#         update_pos(-90,0,0)
#     elif X_GOAL == 0 and Y_GOAL > 0:
#         left_deg(90)
#         update_pos(90,0,0)

def move_to_next(position1, position2):
    global theta
    scale = 1.2
    x_diff = position2[0] - position1[0]
    y_diff = position2[1] - position1[1]
    move_dis = np.sqrt(x_diff**2 + y_diff**2)
    # if x_diff > 0:
    #     if y_diff > 0:
    #         left_angle = np.arctan((y_diff/ x_diff)) / 3.14 * 180
    #         left_deg(left_angle*scale)
    #         print 'left_angle', left_angle
    #         update_pos(left_angle,0,0)
    #     elif y_diff < 0:
    #         right_angle = np.arctan((y_diff/ x_diff)) / 3.14 * 180
    #         right_deg(abs(right_angle*scale))
    #         print 'left_angle', left_angle
    #         update_pos(right_angle,0,0)
    #     else:
    #         print 'not turn'
    # if x_diff < 0:
    #     if y_diff > 0:
    #         left_angle = np.arctan((y_diff/ x_diff)) / 3.14 * 180
    #         left_deg(left_angle*scale)
    #         print 'left_angle', left_angle
    #         update_pos(left_angle,0,0)
    #     elif y_diff < 0:
    #         right_angle = np.arctan((y_diff/ x_diff)) / 3.14 * 180
    #         right_deg(abs(right_angle*scale))
    #         print 'left_angle', left_angle
    #         update_pos(right_angle,0,0)
    #     else:
    #         print 'not turn'
    if x_diff != 0:
        if x_diff > 0 and y_diff >=0: #Phase 1
            angle_goal = np.arctan((y_diff/ x_diff)) / 3.14 * 180
        if x_diff < 0 and y_diff >=0: #Phase 2
            angle_goal = 180 + np.arctan((y_diff/ x_diff)) / 3.14 * 180
        if x_diff < 0 and y_diff < 0: #Phase 3
            angle_goal = 180 + np.arctan((y_diff/ x_diff)) / 3.14 * 180
        if x_diff > 0 and y_diff < 0: #Phase 4
            angle_goal = 360 + np.arctan((y_diff/ x_diff)) / 3.14 * 180
    else:
        if y_diff > 0:
            angle_goal = 90
        elif y_diff < 0:
            angle_goal = 270

    angle_diff = angle_goal - theta
    if angle_diff>0:
        left_deg(angle_diff*scale)
        update_pos(angle_diff,0,0)
    elif angle_diff<0:
        right_deg(-angle_diff*scale)
        update_pos(angle_diff,0,0)
    time.sleep(3)
    fwd_cm(move_dis)
    update_pos(0,move_dis,0)
    time.sleep(5)






    

if __name__ == '__main__':
    set_speed(100)
    move_to_next([0,0],[10,10])
