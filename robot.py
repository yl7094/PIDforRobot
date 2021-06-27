from matplotlib.pyplot import plot
import numpy as np
import matplotlib as mp
import matplotlib.pyplot as plt
import matplotlib.animation as animation

class Robot:
	def __init__(self, x0):
		'''
		this is a linear inverted pendulum model with ankle strategy
		'''
		self.x = x0
		self.A = np.zeros([2, 2]) 
		self.B = np.zeros([2, 1]) 
		K,m,g,L,C = 50.,5.,9.81,0.3,10.
		dt= 1e-3
		I= np.eye(2)
		matrix_a= np.matrix([[0,1], [-(K-m*g*L)/(m*L**2),-(C/(m*L**2))]])
		matrix_b= np.matrix([[0],[(K/(m*L**2))]])
		self.A= dt * matrix_a + I
		self.B= dt * matrix_b

		self.u_bounds = [-np.pi/4, np.pi/4]

		self.noise = True
		self.impulse = True
               
	def step(self, u, counter):
		self.x= self.A.dot(self.x) + self.B.dot(u)
		if counter >0 and self.noise:
			disturbance = np.random.normal(0., 0.01)
			self.x[1] +=disturbance
		if counter ==500 and self.impulse:
			impulse = 10.
			self.x[1] += impulse
	def getState(self):
		return self.x.copy()

	def bound(self, u):
		if u<self.u_bounds[0]:
			u_ret = self.u_bounds[0]
			return u_ret
		if u>self.u_bounds[1]:
			u_ret = self.u_bounds[0]
			return u_ret
		return u
	def plot(self, x_list, theta_des, u_list):
		print('generate plot ...')
		plt.figure()
		plt.plot([x[0] for x in x_list])
		plt.plot(theta_des, 'r--')
		plt.ylabel(r'$\theta_x$')
		plt.grid()
		plt.savefig('data/theta.png',bbox_inches='tight',pad_inches = 0, dpi = 300)

		plt.figure()
		plt.plot([x[1] for x in x_list])
		plt.ylabel(r'$\dot{\theta_x}$')
		plt.grid()
		plt.savefig('data/theta_dot.png',bbox_inches='tight',pad_inches = 0, dpi = 300)

		plt.figure()
		plt.plot(u_list)
		plt.ylabel(r'$\theta_u$')
		plt.grid()
		plt.savefig('data/u.png',bbox_inches='tight',pad_inches = 0, dpi = 300)
		print('generate plot ...done')
	def animate(self, x_list, theta_des, u_list, speed=.3):
		'''
		This function makes an animation showing
		the behavior of the single inverted pendulum model
		'''

		plotx = []
		plotx_des = []
		plotu = []
		T = len(x_list)
		freq = 30
		sample_freq = int(freq*speed)
		for i in range(int(T/sample_freq)):
			plotx.append(x_list[sample_freq*i])
			plotx_des.append(theta_des[sample_freq*i])
			plotu.append(u_list[sample_freq*i])

		use_dt = int(1000/freq)

		fig = mp.figure.Figure(figsize=[2.4,2.4])
		mp.backends.backend_agg.FigureCanvasAgg(fig)
		ax = fig.add_subplot(111, autoscale_on=False, xlim=[-.4,.4], ylim=[-.1,.4])
		ax.grid()
		list_of_lines = []

		#plot the ground
		ax.plot([-0.3,0.3],  [0,0])

		#create the robot
		#for the desired CoM
		line, = ax.plot([], [], 'or--', ms=10, lw=0, markevery=[-1], alpha=.3)
		list_of_lines.append(line)
		#for the simulated CoM
		line, = ax.plot([], [], 'ok--', ms=10, lw=0.5, markevery=[-1])
		list_of_lines.append(line)
		#for the ankle
		line, = ax.plot([], [], 'k', lw=1)
		list_of_lines.append(line)

		L = 0.3
		lowerLeg =0.1
		def animate(i):
			for l in list_of_lines: #reset all lines
				l.set_data([],[])
			list_of_lines[0].set_data([0, L*np.sin(plotx_des[i])], [0, L*np.cos(plotx_des[i])])
			list_of_lines[1].set_data([0, L*np.sin(plotx[i][0])], [0, L*np.cos(plotx[i][0])])
			list_of_lines[2].set_data([0, lowerLeg*np.sin(plotu[i])], [0, lowerLeg*np.cos(plotu[i])])
			
			return list_of_lines
		
		def init():
			return animate(0)
		print('generate animation ...')
		ani = animation.FuncAnimation(fig, animate, np.arange(0, len(plotx)),
			interval=use_dt, blit=True, init_func=init)

		ani.save('data/inverted_pendumlum.mp4',
			dpi=300,
			fps=freq,
			writer='ffmpeg')

		print('generate animation ...done')