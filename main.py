import numpy as np

from robot import Robot
from pid import PID

T = 2000
dt = 1e-3
rest_T = 500
time1 = np.linspace(0, T*dt, T-rest_T)
time2 = np.linspace(T*dt, T*dt, rest_T) # for tracking restitution
time = np.concatenate([time1, time2])
p_gain = 25.        # for balance with noise, p_gain=20
d_gain = 0.2        # for balance with noise, d_gain=0.1
x0 =np.array([[0.],[0.]]) #rad, rad/s

u_list = [0.]*T
x_list = [None] *T

# theta_des = [0.]*T # for balance

amplitude = np.pi/10. # for tracking
theta_des = np.sin(time/(T*dt)*2*np.pi)*amplitude

u_des = 0.
t = 0.


robot = Robot(x0)
pid = PID(p_gain,0.,d_gain, t)

for i in range(T):

    print('simulation step: %d'%(i+1))
    
    x = robot.getState()
    
    #######controller#######
    theta = x[0,0]
    pid.SetPoint = theta_des[i]
    pid.update(theta, t)
    o=pid.output
    u = robot.bound(o - u_des)
    #######controller#######

    x_list[i] = x
    u_list[i] = u
    robot.step(u, i)
    t += dt

robot.plot(x_list, theta_des, u_list)

robot.animate(x_list, theta_des, u_list, speed=.3)