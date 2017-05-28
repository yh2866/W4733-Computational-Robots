from gopigo import *
import time

INCR = 10
SAMPLE = 10
REQUIRED = 8

def scanOneEighty():
        objectDetected = False
        
        for i in range(0, 180, INCR):
                sampling = []
                servo(i)
                time.sleep(0.3)
                print("angle ", i)
                
                for i in range(SAMPLE):
                        time.sleep(0.05)
                        d = us_dist(15)
                        
                        print(d)
                        
                        if d <= 100 and d > 0:
                                sampling.append(d)

                if len(sampling) >= REQUIRED:
                        objectDetected = True
                        break
                
        return objectDetected
                

if __name__ == "__main__":
        objectDected = False
        servo(90)
 	time.sleep(1)

 	set_speed(60)
 	time.sleep(1)
 	
 	
        objectDetected = scanOneEighty()

        if not objectDetected:
                set_speed(100)
                
                start = time.time()
                left_rot()

                while True:
                        if time.time() - start >= 5:
                                stop()
                                break

                objectDetected = scanOneEighty()

                

        

                
                        
                
                
        
			

