from gopigo import *
import random
import time


if __name__ == "__main__":
    move_options = { 0 : motor_fwd,
                     1 : motor_bwd,
                     2 : left,
                     3 : left_rot,
                     4 : right,
                     5 : right_rot,

    }

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

        if end - start > 20:
            break


        moveStart = time.time()
        i = random.randint(0, 7)

        while True:
            set_speed(speed_options[i])
            moveEnd = time.time()
            print(i)

            if i >= 6:
                servo(random.randint(0, 180))
            else:
                move_options[i]()

            if moveEnd - moveStart > 1:
                break
        print("inner while ended")

    stop()







