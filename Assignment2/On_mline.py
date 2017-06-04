def On_mline(x_goal, y_goal, x, y):
    #y=kx
    k = y_goal/x_goal
    if(y==k*x):
        return True
    else:
        return False
