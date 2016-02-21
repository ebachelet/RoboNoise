import numpy as np


class RedNoiseSolver(object):


	def __init__(self, data) :

		self.data = data


	def clean_bad_data(self) :

		#Clean stars with -1.0 or >10 in errormag.

		stars = np.unique(self.data[:,0])
		index = np.arange(0,len(self.data)+1)
		index3 = []
		
		for i in stars :

			index2 = np.where(self.data[:,0]==i)[0]			
			if (-1.0 in self.data[index2,4].astype(float)) | (max(self.data[index2,4].astype(float))>10) :
				pass
			else :
		
				index3 = index3+index2.tolist()
		
		self.data = self.data[index3]
		
	def clean_bad_stars(self,choices) :

		#Clean stars that you do not want, for example the mucrolensing target.

		stars = np.unique(self.data[:,0])
		index = np.arange(0,len(self.data)+1)
		index3 = []
		
		for i in stars :

			index2 = np.where(self.data[:,0]==i)[0]	
					
			if i in choices :
				pass
			else :
		
				index3 = index3+index2.tolist()
		
		self.data = self.data[index3]


	def clean_magnitude_data(self,threshold) :

		stars = np.unique(self.data[:,0])
		index = np.arange(0,len(self.data)+1)
		index3 = []
		
		
		for i in stars :

			index2 = np.where(self.data[:,0]==i)[0]			
			if max(self.data[index2,3].astype(float))>threshold :
				pass
			else :
		
				index3 = index3+index2.tolist()
		
			
		self.data = self.data[index3]			

	def define_bins(self,choice,size=0.0):
		if size ==0.0 :
			
			size = len(np.unique(self.data[:,choice]))
			self.bins = np.unique(self.data[:,choice]).astype(float)
			self.bins = np.append([self.bins],[2*self.bins[-1]])

		else :

			#define bins with equally spaced, self.bins are bins limits
			histogram = np.histogram(self.data[:,choice].astype(float),size)
			self.bins = histogram[1]
			
	def solver(self,choice) :

		stars = np.unique(self.data[:,0])
		number_of_stars = len(stars)
		number_of_bins = len(self.bins)


		A=np.zeros((number_of_stars,number_of_stars))
		B=np.zeros((number_of_stars,number_of_bins-1))
		D=np.zeros((number_of_bins-1,number_of_bins-1))

		v1 = np.zeros(number_of_stars)
		v2 = np.zeros(number_of_bins-1)

		for i in xrange(number_of_stars):
	
			index = np.where(self.data[:,0]==stars[i])[0]
	
			A[i,i] = sum(1/self.data[index,4].astype(float)**2)
			v1[i] = sum(self.data[index,3].astype(float)/self.data[index,4].astype(float)**2)

			for j in xrange(number_of_bins-1):
				
					
				index_bins = np.where((self.data[index,choice].astype(float)>=self.bins[j]) & (self.data[index,choice].astype(float)<self.bins[j+1]))[0]	
				
				B[i,j] = sum(1/self.data[index[index_bins],4].astype(float)**2)
			print i/float(number_of_stars)
					
		for j in xrange(number_of_bins-1):
		
			index_bins = np.where((self.data[:,choice].astype(float)>=self.bins[j]) & (self.data[:,choice].astype(float)<self.bins[j+1]))[0]
			D[j,j] = sum(1/self.data[index_bins,4].astype(float)**2)
		
			v2[j] = sum(self.data[index_bins,3].astype(float)/self.data[index_bins,4].astype(float)**2)

		Invert_A=np.copy(A)
		for i in xrange(number_of_stars):

			Invert_A[i,i] = 1/A[i,i]	


		term1=np.dot(Invert_A,B)
		term2=np.dot(B.T,term1)
		term3=D-term2
		term4=np.dot(Invert_A,v1)
		term5=np.dot(B.T,term4)
		term6 = v2-term5


		# inverting matrix, not really efficient 
		#Invert = np.linalg.inv(term3)
		#x2=np.dot(Invert,term6)


		# x2=np.linalg.solve(term3,term6), solver, not the best
		
		#leastsq solver
		x2=np.linalg.lstsq(term3,term6)[0]
		self.x2 = x2
