from gopigo import *
import random
import time


if __name__ == "__main__":
    #Dance options
    move_options = { 0 : motor_fwd,
                     1 : motor_bwd,
                     2 : left,
                     3 : left_rot,
                     4 : right,
                     5 : right_rot,
    }
    #Speed options
    speed_options = {0 : 30,
                     1 : 60,
                     2 : 90,
                     3 : 120,
                     4 : 150,
                     5 : 180,
                     6 : 210,
                     7 : 240
    }

    start = time.time()

    while True:
        end = time.time()
        #Set the total running time is 20
        if end - start > 20:
            break
        
        moveStart = time.time()
        #Randomly create options from 0~7
        i = random.randint(0, 7)
        
        while True:
            #Set move speed
            set_speed(speed_options[i])
            moveEnd = time.time()
            #Set move actions
            if i >= 6:
                servo(random.randint(0, 180))
            else:
                move_options[i]()
            #Set moving time of each action to 1
            if moveEnd - moveStart > 1:
                break
        print("inner while ended")

    stop()
