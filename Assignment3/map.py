import matplotlib.pyplot as plt
import numpy as np

start_point = [10,20]
goal_point = [250,250]
dimensions_x = 300
dimensions_y = 300

object1 = np.array([[200, 220],
				    [221.213203436, 241.213203436],
		 		    [210.606601718, 251.819805153],
				    [189.393398282, 230.606601718]])

object2 = np.array([[130, 180],
					[159.997181494, 179.588779362],
					[145.35287801, 194.640170509]])

object3 = np.array([[150, 120],
					[194.995772241, 119.383169043],
					[173.029317014, 141.960255763]])

object4 = np.array([[230, 170],
					[251.501987353, 190.920433549],
					[230.503960307, 191.208287996]])


def plot_environment(object):
	plt.plot(object[:,0],object[:,1],'b-')
	plt.plot((object[-1,0],object[0,0]),(object[-1,1],object[0,1]),'b-')
	return

def grown_obstacle(object):
	l = len(object)
	grown_obstacle = np.zeros((4*l,2))
	for i in xrange(l):
		grown_obstacle[0*l+i][0] = object[i][0]
		grown_obstacle[0*l+i][1] = object[i][1]
		grown_obstacle[1*l+i][0] = object[i][0]-23
		grown_obstacle[1*l+i][1] = object[i][1]-23
		grown_obstacle[2*l+i][0] = object[i][0]-23
		grown_obstacle[2*l+i][1] = object[i][1]
		grown_obstacle[3*l+i][0] = object[i][0]
		grown_obstacle[3*l+i][1] = object[i][1]-23
		plt.plot(grown_obstacle[:,0],grown_obstacle[:,1],'ro')
	return grown_obstacle


if __name__ == "__main__":
	plt.plot(start_point[0],start_point[1],'ro')
	plt.plot(goal_point[0],goal_point[1],'ro')
	plot_environment(object1)
	plot_environment(object2)
	plot_environment(object3)
	plot_environment(object4)
	grown_obstacle(object1)
	grown_obstacle(object2)
	grown_obstacle(object3)
	grown_obstacle(object4)
	plt.xlim([0,dimensions_x])
	plt.ylim([0,dimensions_y])
	plt.show()