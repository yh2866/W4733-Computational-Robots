from gopigo import *
import time
import numpy as np


if __name__ == "__main__":
    
    set_speed(90)
    enc_tgt(1,1,18)
    start = time.time()
    left_rot()

    while True:
        print "time ", time.time() - start
    
