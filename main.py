import numpy as np
import matplotlib.pyplot as plt
from robot import Robot
from pid import PID
T = 5000 # needs to define
dt = 1e-3
p_gain = 10. # needs to define
d_gain = 10./np.sqrt(2) # needs to define
x0 = np.zeros([2, 1])  # needs to define
u_list = [0.]*T
x_list = [None] *T
theta_des = 0.
u_des = 0. 
t = 0.
robot = Robot(x0)
pid = PID(p_gain,0.,d_gain, t)
for i in range(T):
	print('simulation step: %d'%i)
	x = robot.getState()
	#######controller#######
	theta = x[0,0]
	pid.SetPoint = theta_des
	pid.update(theta, t)
	o=pid.output
	u = u_des - o
	#######controller#######
	x_list[i] = x
	u_list[i] = u
	print(x_list)
	print(u_list)
	robot.step(u)
	t += dt