from gopigo import *
import time
import numpy as np
import matplotlib.pyplot as plt

en_debug = 1

# 519bc0bfe2b530c58ab22d0d717c4220cdcdd7a1

DPR = 360.0/64
WHEEL_RAD = 3.25 # Wheels are ~6.5 cm diameter.
CHASS_WID = 13.5 # Chassis is ~13.5 cm wide.DPR = 360.0/64

X = 0.0
Y = 0.0
X_Goal = 300.0
Y_Goal = 0.0
theta = 0

OBSTACLE_X = -1
OBSTACLE_Y = -1


theta_change = 30
theta_actual_change = 39

ERROR_mline = 4
ERROR_goal = 5


PLOT_X_LIST = []
PLOT_Y_LIST = []
OBSTACLE_X_LIST = []
OBSTACLE_Y_LIST = []
Original_Pos = [[0],[0],[1]]
Previous_Matrix = [[1, 0, 0],
                   [0, 1, 0],
                   [0, 0, 1]]

BLOCKED_MLINE_X = []
BLOCKED_MLINE_Y = []

UNBLOCKED_MLINE_X = []
UNBLOCKED_MLINE_Y = []
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

    Previous_Matrix = np.dot(Previous_Matrix,transform_matrix(theta_change,X_change,Y_change))
    Current_Pos = np.dot(Previous_Matrix,Original_Pos)
    Currrent_Pos_Obstacle = np.dot(Previous_Matrix, [[OBSTACLE_X], [OBSTACLE_Y], [1]])
    X = Current_Pos[0]
    Y = Current_Pos[1]

    OBSTACLE_X = Currrent_Pos_Obstacle[0]
    OBSTACLE_Y = Currrent_Pos_Obstacle[1]

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


def isGoal(X_Goal, Y_Goal, X, Y):
    return abs(X - X_Goal) <= ERROR_goal and abs(Y - Y_Goal) <= ERROR_goal



def posFeedback(theta_change, X_change, Y_change):
    onGoal = False
    onMLine = False

    update_pos(theta_change, X_change, Y_change)

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


def avoidObject():
    onGoal, onMLine = posFeedback(0, 0, 0)


    if len(BLOCKED_MLINE_X) > 0 and onMLine:
        print("h mline")
        for i in range(len(BLOCKED_MLINE_X)):
            if abs(BLOCKED_MLINE_X[i] - X) <= ERROR_mline and abs(BLOCKED_MLINE_Y[i] - Y <= ERROR_mline):
                print("No solution")
                stop()
                time.sleep(1)
                return True

    print("h mline value push")
    print("X ", X)
    print("Y ", Y)
    BLOCKED_MLINE_X.append(X)
    BLOCKED_MLINE_Y.append(Y)

    obstacle_move = 0

    while detect(20, 0):
        left_deg(54)
        update_pos(45,0,0)
        time.sleep(1)

    scale = 1.1
    servo(0)
    time.sleep(1)

    while True:


        while True:
            # check object next to gopigo

            while detect(20, 10):
                # check front too
                servo(90)
                time.sleep(0.5)
                # no object front, but we have an object next. so we move forward
                if not detect(20, 0):

                    OBSTACLE_X = 0
                    OBSTACLE_Y = -20

                    # using this to update obstacle location
                    update_pos(0, 0, 0)

                    OBSTACLE_X_LIST.append(OBSTACLE_X)
                    OBSTACLE_Y_LIST.append(OBSTACLE_Y)


                    fwd_cm(3)
                    obstacle_move += 3
                    onGoal, onMLine = posFeedback(0, 3, 0)

                    secondVisitMLine = False

                    if onGoal:
                        return True

                    elif onMLine and obstacle_move > 10:
                        print("check h or l mline")

                        if theta >= 0:
                            print(" h m line")

                            if len(BLOCKED_MLINE_X) > 0 and onMLine:
                                print("h mline")
                                for i in range(len(BLOCKED_MLINE_X)):
                                    if abs(BLOCKED_MLINE_X[i] - X) <= ERROR_mline and abs(BLOCKED_MLINE_Y[i] - Y <= ERROR_mline):
                                        print("No solution 2!!!")
                                        stop()
                                        time.sleep(1)
                                        return True

                            print("on m line, but got farther. Ignore")

                        else:
                            print("l m line")

                            if len(UNBLOCKED_MLINE_X) > 0:
                                for i in range(len(UNBLOCKED_MLINE_X)):
                                     if abs(UNBLOCKED_MLINE_X[i] - X) <= ERROR_mline and abs(UNBLOCKED_MLINE_Y[i] - Y <= ERROR_mline):
                                     #if abs(UNBLOCKED_MLINE_X[i] - X) <= 30 and abs(UNBLOCKED_MLINE_Y[i] - Y <= ERROR_mline):
                                        print("second visit m line. just move forward.")
                                        #plot_path()
                                        #time.sleep(1)
                                        #plt.savefig("result.png")
                                        #time.sleep(3)

                            if not secondVisitMLine:
                                if (X_Goal**2 + Y_Goal**2) > ((X_Goal - X)**2 + (Y_Goal - Y)**2):
                                    UNBLOCKED_MLINE_X.append(X)
                                    UNBLOCKED_MLINE_Y.append(Y)

                                    print("MLINE VALUE PUSH")
                                    print("X ", X)
                                    print("Y ", Y)
                                    print("--------------")

                                    rot_angle = -theta

                                    if rot_angle < 0:
                                        right_deg(abs(rot_angle)*scale)
                                        update_pos(rot_angle, 0, 0)
                                    else:
                                        left_deg(abs(rot_angle)*scale)
                                        update_pos(rot_angle, 0, 0)

                                    time.sleep(0.5)
                                    servo(90)
                                    time.sleep(0.5)


                                    if(bug2()):
                                        return True


                # object to the front and also object next to gopigo. Avoid it
                else:

                    OBSTACLE_X = 20
                    OBSTACLE_Y = 0

                    # using this to update obstacle location
                    update_pos(0, 0, 0)

                    OBSTACLE_X_LIST.append(OBSTACLE_X)
                    OBSTACLE_Y_LIST.append(OBSTACLE_Y)

                    left_deg(54)
                    update_pos(45,0,0)
                    time.sleep(1)
                    onMLine = False
                    onGoal = False

                servo(0)



            servo(0)
            time.sleep(1)

            if detect(10, 0):
                left_deg(theta_actual_change)
                update_pos(theta_change, 0, 0)
                time.sleep(1)
            else:
                break


        servo(0)
        time.sleep(1)

        # object next to gopigo too far away. Need to get closer to it.
        while not detect(20, 0):
            servo(90)
            time.sleep(1)

            if not detect(20, 0):
                print("not detect")
                right_deg(theta_actual_change)
                update_pos(-theta_change,0,0)
                time.sleep(1)
            else:
                print("detect")
                left_deg(54)
                update_pos(45,0,0)
                time.sleep(1)
            servo(0)
            time.sleep(1)

def plot_path():
    print 'PLOT_X_LIST', PLOT_X_LIST
    print 'PLOT_Y_LIST', PLOT_Y_LIST
    plt.plot(PLOT_X_LIST[0], PLOT_Y_LIST[0], 'go')
    plt.plot(PLOT_X_LIST[1:-2],PLOT_Y_LIST[1:-2],'bo', )
    plt.plot(PLOT_X_LIST[-1], PLOT_Y_LIST[-1], 'ro')
    plt.plot(PLOT_X_LIST,PLOT_Y_LIST,'b')
    plt.plot(OBSTACLE_X_LIST, OBSTACLE_Y_LIST, 'rx')
    plt.xlim((-20, max(X_Goal, Y_Goal) + 20 ))
    plt.ylim((-20, max(X_Goal, Y_Goal) + 20 ))



def orient_to_goal():
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


def bug2():
    onGoal = False
    onMLine = False

    servo(90)
    set_speed(100)
    scale = 1.2

    #Let the robot turn to the direction of the final goal
    orient_to_goal()

    if isGoal(X_Goal, Y_Goal, X, Y):
        plot_path()
        plt.savefig("result.png")
        stop()
        return True
    else:
        while not detect(20, 0):
            fwd_cm(3)
            onGoal, onMLine = posFeedback(0, 3, 0)

            if onGoal:
                plot_path()
                plt.savefig("result.png")
                stop()
                return True

    avoidObject()





if __name__ == '__main__':
    #Run bug2 algorithm
    bug2()
    plot_path()

    #Save trajectory picture
    plt.savefig("result.png")
