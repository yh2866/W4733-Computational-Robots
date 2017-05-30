from gopigo import *
import time

if __name__ == "__main__":
    servo(90)
    time.sleep(0.5)
    start = time.time()
    left_rot()

    while time.time() - start < 2:
        t = time.time() - start
        print(t)
        continue

    stop()
    
