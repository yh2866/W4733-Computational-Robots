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

    start = time.time()

    while True:
        end = time.time()

        if end - start > 20:
            break


        moveStart = time.time()
        i = random.randint(0, 6)

        while True:
            moveEnd = time.time()
            print(i)

            if i == 6:
                servo(random.randint(0, 180))
            else:
                move_options[i]()

            if moveEnd - moveStart > 2:
                break
        print("inner while ended")

    stop()







