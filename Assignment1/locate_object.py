from gopigo import *
import time

INCR = 10
SAMPLE = 10
REQUIRED = 7

def scanOneEighty():
        objectDetected = False
        angle = 0
        
        for i in range(0, 180, INCR):
                sampling = []
                servo(i)
                time.sleep(0.3)
                print("angle ", i)
                
                for j in range(SAMPLE):
                        time.sleep(0.05)
                        d = us_dist(15)
                        
                        print(d)
                        
                        if d <= 100 and d > 0:
                                sampling.append(d)

                if len(sampling) >= REQUIRED:
                        objectDetected = True
                        angle = i
                        break
                
        return objectDetected, angle
                

if __name__ == "__main__":
        objectDetected = False
        angle = 0
        servo(90)
 	time.sleep(1)

 	set_speed(50)
 	time.sleep(1)
 	
 	while not objectDetected:
                start = time.time()
                left_rot()

                while True:
                        if time.time() - start >= 2:
                                stop()
                                break
                        
                objectDetected, angle = scanOneEighty()
        
        servo(90)
        set_speed(50)
        
        t = (angle - 90) / 20        
        rotateLeft = True
        
        if time < 0:
                rotateLeft = False

        t = abs(t)

        start = time.time()
        
        if rotateLeft:
                left_rot()
        else:
                right_rot()

        """ need to consider the sonic conic angle to adjust the robot to face
           the front of the detected object """
        while True:
                if time.time() - start >= t:
                        stop()
                        break

        d = us_dist(15)

        if d < 25:
                motor_bwd()
                while d < 20:
                        d = us_dist(15)
                stop()
        else:
                motor_fwd()
                while d > 25:
                        d = us_dist(15)
                stop()

        

                
                        
                
                
        
			

