import numpy as np
class Robot:
	def __init__(self, x0):
		'''
		this is a linear inverted pendulum model with ankle strategy
		'''
		self.x = x0
		self.A = np.zeros([2, 2]) # needs to define
		self.B = np.zeros([2, 1]) # needs to define
		K,m,g,L,C=753,5,9.81,0.3,18
		dt= 1e-3
		I= np.eye(2)
		print(I)
		matrix_a= np.matrix([[0,1], [-(K*m*g*L/(m*L**2)),-(C/(m*L**2))]])
		matrix_b= np.matrix([[0],[(K/(m*L**2))]])
		A= dt * matrix_a + I
		B= dt * matrix_b
		#Example
		#A= np.matrix([[1, 1*10**-3], [-(24.623), (0.96)]])
		#B= np.matrix([[0],[(1.673)]])
			   #Assuming the random values as: m=5kg, L=0.3m, g=9.81m/s**2, K=753Nm/rad, C=18Nm/sec, dt=1e-3, I=Identity Matrix of order(2x2)
			   #Substituting these values in the general equation: Xn+1= AXn + BUn  such that A= dt * matrix_a + I  and  B= dt * matrix_b
			   #Wherein, matrix_a= np.matrix([[0,1], [-(KmgL/mL**2),-(C/mL**2)]]) and matrix_b= np.matrix([[0],[(K/mL**2)]])
	def step(self, u):
		self.x= self.A.dot(self.x) + self.B.dot(u)
	def getState(self):
		return self.x.copy()