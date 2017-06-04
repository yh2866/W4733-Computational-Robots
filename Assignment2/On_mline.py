def distance(x,y,k):
    return abs(y-k*x)/np.sqrt(1+k**2)

def On_mline(x_goal, y_goal, x, y):
    #y=kx
    error = 0.2
    if(x_goal==0): #k not exist
        if(x<=error):
            return True
        else:
            return False

    k = y_goal/x_goal
    dist = distance(x,y,k)
    if(dist<=error):
        return True
    else:
        return False
