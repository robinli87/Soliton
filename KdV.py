#header
#KdV contains calculation classes that are called by main.py
#Author: Robin
#Inputs: inputs inherited from the main:
#initialise solution fields with N, initial_waveform and duration
#specific functions intake other parameters involved in calculation: delta, A, dt, dx
#Outputs: the finished solution field


import math

def init_gen(N, A, delta, dx):
	initial_x = []
	def sech(x):
		e = 2.71828
		y = 2 / (e ** x + e ** -x)
		return(y)
		
	for i in range(0, N):
		wavenumber = dx * i * (A / 12)**0.5 / delta  #the stuff inside sech()
		displacement = A * (sech(wavenumber))**2
		initial_x.append(displacement)
		
	return(initial_x) 
		
class kdv:
	u = []
	
	def __init__(self, N, initial_waveform, duration, dt, dx, A, delta):
		#globalise all variables within this class
		self.N = int(N)
		self.delta = delta
		self.A = A
		self.dt = dt
		self.dx = dx
		self.duration = int(round(duration / dt)) #number of dts that the field needs to include
		
		self.u = []
		for i in range(0, self.duration):
			line = []
			for j in range(0, self.N):
				line.append(0)				
			self.u.append(line)
				
		self.du = []		
		for i in range(0, self.duration):
			line = []
			for j in range(0, self.N):
				line.append(0)				
			self.du.append(line)
			
		self.d3u = []
		for i in range(0, self.duration):
			line = []
			for j in range(0, self.N):
				line.append(0)				
			self.d3u.append(line)
		
		#now append initial condition to the solution field
		for i in range(0, N):
			self.u[0][i] = initial_waveform[i]
			
		u = self.u
		
	def analytical(self):
		for i in range(0, self.duration):
			for j in range(0, self.N):
				#calculate the the value of u (the disturbance of the wave) in this cell
				def U(x, t):
					#define a sech function from first principles
					def sech(y):
						e = 2.71828
						z = 2 / (e ** y + e ** -y)
						return(z)
					wavenumber = (x - self.A * t / 3) * ((self.A / 12)**0.5 / self.delta)  #the stuff inside sech()
					disturbance = self.A * (sech(wavenumber))**2  #now sech squared	
					return(disturbance) 
						
				self.u[i][j] = U(j * self.dx, i * self.dt) #write this value into our array of u


	def numerical(self):

		#Let's first deal with setting up some more initial conditions
		#generate the first row of du and d3u 

		#left edge:
		for j in range(0, 2):
			dudx = (self.u[0][j+1] - self.u[0][j]) / self.dx
			d3udx3 = (self.u[0][j+3] - 3 * self.u[0][j+2] +3 * self.u[0][j+1] + self.u[0][j]) / (self.dx)**3

			self.u[1][j] = self.u[0][j] - self.dt*(self.u[0][j] + d3udx3 * self.delta**2 )

		#bulk middle:
		
				
		return(self.u)
				
