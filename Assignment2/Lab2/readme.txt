Testing Scenarios

1. Scenario One
We placed two objected in front of gopigo to go around and avoid.
Link:
https://youtu.be/koR3BD4hQck


2. Second Scenario
We tested the case where gopigo is placed in an closed environment where it is not possible to reach its goal.
Link:
https://youtu.be/en30Bn4touU


3. Third Scenario
We tested the case where gopigo would need to revisit the same leave m-line point, so instead of following m-line, it would ignore the m-line and just keep following around the obstacle that it had encountered before.
Link:
https://youtu.be/fZghDoqp1KA



Notice: Problems with calibrations.

While running gopigo, we noticed a lot of inconsistencies with motor rotations. First thing that we would like to mention is the problem that we faced when using left_deg() and right_deg() functions. As an example, passing 45 degrees as its parameter for left_deg() actually did not rotate 90 degrees, but around 35 - 40 degrees. So we had to use two different angles. Expected and actual angles. So we would use 45 as expected and 55 as its actual angle to make the motors rotate 45 degrees.

Second problem was that even passing 55 degrees as left_deg()' parameter did not make the motor rotate 45 degrees but angles around 45 +- 3. This is saying that if we run left_deg(110) 10 times, we would get slightly different 10 results. Thus while the margin of errors may appear small, repeatedly calling left_deg() and right_deg() would make those small errors to add up and actually make large discrepancies in terms of the robots global position.

So even though we tried to calibrate the expected and actual angles every time when we run gopigo, our results were not consistent because of the problem stated above, meaning while (we believe) our algorithm is theoretically correct, we don't consistently get the same results.

Thus for each scenario that we tested, we recorded videos multiple times and picked the one that appeared most promising.