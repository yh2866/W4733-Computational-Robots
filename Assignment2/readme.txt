
Notice: Problems with calibrations.

While running gopigo, we noticed a lot of inconsistencies with motor rotations. First thing that we would like to mention is the problem that we faced when using left_deg() and right_deg() functions. As an example, passing 90 degrees as its parameter for left_deg() actually did not rotate 90 degrees, but around 75 - 85 degrees. So we had to use two different angles. Expected and actual angles. So we would use 90 as expected and 110 as its actual angle to make the motors rotate 90 degrees.

Second problem was that even passing 110 degrees as left_deg()' parameter did not make the motor rotate 90 degrees but angles around 90 +- 3. This is saying that if we run left_deg(110) 10 times, we would get slightly different 10 results. Thus while the margin of errors may appear small, repeatedly calling left_deg() and right_deg() would make those small errors to add up and actually make large discrepencies in terms of the robots global position.

So even though we tried to calibrate the expected and actual angles every time when we run gopigo, our results were not consistent because of the problem stated above, meaning while (we believe) our algorithm is theoretically correct, we don't consistently get the same results.


Thus for each senario that we tested, we recorded videos multiple times and picked the one that appeared most promising.




Testing Scenarios


1. First Scenario

We tested the case where gopigo is placed in an closed environment where it is not possible to reach its goal.





2. Second Scenario

We placed two objected in front of gopigo to go around and avoid.





3. Third Scenario

We tested the case where gopigo would need to revisit the same leave mline point, so instead of following mline, it would igore the mline and just keep following around the obstacle that it had encountered before.









