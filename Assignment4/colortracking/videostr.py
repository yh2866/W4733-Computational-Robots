import cv2
import numpy as np

cap = cv2.VideoCapture(0)
while(1):
    ret,frame = cap.read()
    cv2.imshow('image', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()