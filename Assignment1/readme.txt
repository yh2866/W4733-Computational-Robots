Group Name: Wall E
Group Members: Yuanqing Hong (yh2866), Seung Hwan Lee (sl3966), Yuanfeng Mao (ym2576)


Problem 1:
Done.

Problem 2:
Code implementation is found in dance.py.
We let it dance with different actions: move forward, move backward, turn right, turn left, swipe head.
Also, we let it dance with different speed.
Please see the vedio: 
https://youtu.be/-OR-_qc2c5w

Problem 3:
Code implementation is found in sensor_accuracy.py.
Using a while loop to let it detect distance all the time and put it into fixed distance compare the result with ruler.
For 5 cm, the ultra sonic gave the correct measurement of 5 cm.
For 30 cm, we got 38 cm.
For 60 cm, we got 77 cm.

Problem 4:
Code implementation is found in footprint.py.
For the Method 1, the geometic plot can be found on image "Q4_Method 1"
We keep the robot in the front of object's center, test it several times with different distance.
And the result angle is between 22~40 degree.
For the Method 2, the geometic plot can be found on image "Q4_Method 2"
We keep the robot in the front of object's edge, test it several times with different distance.
And the result angle is between 52~60 degree.
We prefer the method 2, therefore, for the angles of beam, it should be at range of 52~60 degree.

Problem 5:
Code implementation is found in locate_object.py.
We let it turn left and detect distance alternatively. When it detect object that is less than 20cm, we will record this time and also we will record the time that cannot detect object. By turning a little back, we can let the robot stand in the front of object. And then move the robot forward untill detected distance is less than 20.
In addition, we also consider the situation that the robot is originally close to object and the distance is less than 20cm. In this situation, we will let the robot to move backward.
Please see the vedioes:
https://youtu.be/Jezt_zl8YOs
https://youtu.be/M09ESijY_gw
