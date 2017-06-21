W4733 Assignment 3
Team: Wall-E
Team members: Yuanqing Hong (yh2866), Seung Hwan Lee (sl3966), Yuanfeng Mao (ym2576)


For the part1:
We import the data from the file ¡®ROBORACE.txt¡¯, which includes the information about environment and obstacles. In addition, the reference point in our algorithm is on the upper right point. After growing up, the point become the down left point. Through our algorithm, it will calculate the shortest path and shows it. The plotting result can be found by the file ¡®result.jpg¡¯.  At last, it will generate the points for the shortest path. 

For the part2:
From the points generated from the part1. We let the robot move following the points one by one. We have the general method for all of the possibilities. It will theoretically process all of the situations. But, in practical experience, the GoPiGo adds on too much error. Therefore, we customize the move for the specialized race. The method we used is to manually calibrate for each steps.