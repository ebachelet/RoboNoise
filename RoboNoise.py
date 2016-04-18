import numpy as np
import collections

class RedNoiseSolver(object):


	def __init__(self, data, dictionary) :

		self.data = data
		self.dictionary = dictionary
	

	# definition of the new solver for general continuous quantities
	def find_systematics(self,params) :

		magnitude_measurements = self.data[:,self.dictionary['mag']].astype(float)]
		magnitude_measurements = magnitude_measurements-self.model_airmass(params)
		magnitude_measurements = magnitude_measurements-self.model_CCD_positions(params)
		magnitude_measurements = magnitude_measurements-self.model_exposure_time(params)
		magnitude_measurements = magnitude_measurements-self.model_background(params)
		magnitude_measurements = magnitude_measurements-self.model_seeing(params)
		magnitude_measurements = magnitude_measurements-self.model_phot_scale_factor(params)
		
		return magnitude_measurements/self.data[:,self.dictionary['err_mag']].astype(float)]



	# definitions of continuous quantities functions. Mainly linear functions for a start.

	def model_airmass(self, params) :

		offset_airmass = params*self.quantities.airmass
		return offset_airmass

	def model_CCD_positions(self, params) :
		
		offset_CCD = 0.0 
		degree = 2
		for i in range(degree+1) :
			for j in range(degree+1) :
			
			if (i+j>degree) | (i+j==0) :	
				pass
			else :

				offset_CCD+ = params[i+j-1]*self.quantities.X**(i)*self.quantities.Y**(j)

		return offset_CCD


	def model_exposure_time(self, params) :
		
		offset_exptime = params*self.quantities.exptime
		return offset_exptime

	def model_seeing(self, params) :
		
		offset_seeing = params*self.quantities.seeing
		return offset_seeing
	def model_background(self, params) :
		
		offset_background = params*self.quantities.background
		return offset_background

	def model_phot_scale_factor(self, params) :
		
		offset_phot_scale_factor = params*self.quantities.photscalefactor
		return offset_phot_scale_factor
	 
	def clean_bad_data(self) :

		#Clean magnitude measurements with -1.0 or >10 in errormag. or std mag>1

		stars = np.unique(self.data[:,self.dictionary['stars']])
		index = np.arange(0,len(self.data)+1)
		index3 = []
		
		for i in stars :
			
			index2 = np.where(self.data[:,self.dictionary['stars']]==i)[0]			
			if (-1.0 in self.data[index2,self.dictionary['err_mag']].astype(float)) | (max(self.data[index2,self.dictionary['err_mag']].astype(float))>10) | (np.std(self.data[index2,self.dictionary['mag']].astype(float))>1.0) :
				pass
			else :
				
				index3 = index3+index2.tolist()

		self.data = self.data[index3]
		
	def clean_bad_stars(self,choices) :

		#Clean stars that you do not want, for example the mucrolensing target.

		stars = np.unique(self.data[:,self.dictionary['stars']])
		index = np.arange(0,len(self.data)+1)
		index3 = []
		
		for i in stars :

			index2 = np.where(self.data[:,self.dictionary['stars']]==i)[0]	
					
			if i in choices :
				
				pass
			else :
		
				index3 = index3+index2.tolist()

		self.data = self.data[index3]


	def clean_magnitude_data(self,threshold) :

		stars = np.unique(self.data[:,self.dictionary['stars']])
		index = np.arange(0,len(self.data)+1)
		index3 = []
		
		
		for i in stars :

			index2 = np.where(self.data[:,self.dictionary['stars']]==i)[0]			
			if max(self.data[index2,self.dictionary['mag']].astype(float))>threshold :
				pass
			else :
		
				index3 = index3+index2.tolist()

		self.data = self.data[index3]			

	def define_bins(self,choice,size=0.0):
		#import pdb; pdb.set_trace()
		if size ==0.0 :
			
			size = len(np.unique(self.data[:,self.dictionary[choice[0]]]))
			self.bins = np.unique(self.data[:,self.dictionary[choice[0]]]).astype(float)
			self.bins = np.append([self.bins],[2*self.bins[-1]])

		else :

			#define bins with equally spaced, self.bins are bins limits
			histogram = np.histogram(self.data[:,choice].astype(float),size)
			self.bins = histogram[1]


	def compute_quantities(self,choices):

		quantities=collections.namedtuple('Bins',choices)
		
		for i in choices :
			#import pdb; pdb.set_trace()
			
                        # Determine the unique set of epochs (or images) which contain the stars from whic
                        # the measurements are derived
			if i=='time' :	
				quantities.time = np.unique(self.data[:,self.dictionary[i]].astype(float))

                        # NOT SURE WHY YOU DO THIS FOR A POTENTIALLY CONTINUOUS QUANTITY - ADMITTEDLY USUALLY A SINGLE AIRMASS
                        # VALUE IS ASSOCIATED WITH EACH IMAGE, BUT IN REALITY AIRMASS VARIES ACROSS THE IMAGE AREA. SO FOR
                        # THE CODE TO BE GENERAL AIRMASS SHOULD BE TREATED AS A CONTINUOUS QUANTITY, AND THEREFORE A VECTOR
                        # OF UNIQUE VALUES IS NOT A GOOD WAY TO GO
			if i=='airmass' :
				quantities.airmass = np.unique(self.data[:,self.dictionary[i]].astype(float))	

                        # Determine the unqiue set of exposure times used
			if i=='exposure' :	
				quantities.exposure = np.unique(self.data[:,self.dictionary[i]].astype(float))			

		self.quantities = quantities

	# Construct the matrices in the linear least squares problem
	def construct_matrices(self,choices):
             
			#
			self.compute_quantities(choices)


                        # Determine the star list
			stars = np.unique(self.data[:,self.dictionary['stars']])
			number_of_stars = len(stars)

                        # MAKE CHECK HERE THAT THERE ARE AT LEAST TWO STARS - MORE ROBUST CODE - AND REPORT AN ERROR MESSAGE IF NOT

                        # I THINK THIS IS UNNECESSARY AND UNWEILDY - THE PROBLEM POTENTIALLY HAS MANY MANY STARS. ONLY THE DIAGONAL OF THIS MATRIX IS NON-ZERO.
			# NO NEED TO STORE THE WHOLE MATRIX
			A=np.zeros((number_of_stars,number_of_stars))

			A_diagonal=[sum(1/self.data[np.where(self.data[:,self.dictionary['stars']]==i)[0],self.dictionary['err_mag']].astype(float)**2) for i in stars]
			np.fill_diagonal(A,A_diagonal)
			
			# A_DIAGONAL AND V1 CAN BE CALCULATED IN THE SAME LOOP TO AVOID REPEATING COSTLY OPERATIONS MORE THAN NECESSARY e.g. np.where(self.data[:,self.dictionary['stars']]==i)
			v1=[sum(self.data[np.where(self.data[:,self.dictionary['stars']]==i)[0],self.dictionary['mag']].astype(float)/self.data[np.where(self.data[:,self.dictionary['stars']]==i)[0],self.dictionary['err_mag']].astype(float)**2) for i in stars]

			# Construct the B sub-matrix
			B=[]
			for i in xrange(number_of_stars):
				line=[]
				index = np.where(self.data[:,self.dictionary['stars']]==stars[i])[0]
				for j in self.quantities._fields:
					matches = getattr(self.quantities, j)
					#import pdb; pdb.set_trace()
					for k in matches :
						#import pdb; pdb.set_trace()
						index2=np.where(self.data[index,self.dictionary[j]].astype(float)==k)[0]	
						line+=[np.sum(1/self.data[index[index2],self.dictionary['err_mag']].astype(float)**2)]
				B.append(line)
				print i
			B=np.array(B)
			
			# Construct the D matrix and v2 vector
			D=np.zeros((B.shape[1],B.shape[1]))
			v2=np.zeros(B.shape[1])
			count=0
			for i in self.quantities._fields :
				matches = getattr(self.quantities,i)
				for k in matches :
					index=np.where(self.data[:,self.dictionary[i]].astype(float)==k)[0]
					D[count,count]=sum(1/self.data[index,self.dictionary['err_mag']].astype(float)**2)
					v2[count] = sum(self.data[index,self.dictionary['mag']].astype(float)/self.data[index,self.dictionary['err_mag']].astype(float)**2)
					count+=1
	
			
			self.A=A
			self.B=B
			self.D=D
			self.v1=v1
			self.v2=v2	
			#import pdb; pdb.set_trace()

	def solver(self,choice) :

		#stars = np.unique(self.data[:,self.dictionary['stars']])
		#number_of_stars = len(stars)
		#number_of_bins = len(self.bins)


		#A=np.zeros((number_of_stars,number_of_stars))
		#B=np.zeros((number_of_stars,number_of_bins-1))
		#D=np.zeros((number_of_bins-1,number_of_bins-1))

		#v1 = np.zeros(number_of_stars)
		#v2 = np.zeros(number_of_bins-1)

		#for i in xrange(number_of_stars):
	
		#	index = np.where(self.data[:,self.dictionary['stars']]==stars[i])[0]
	
		#	A[i,i] = sum(1/self.data[index,self.dictionary['err_mag']].astype(float)**2)
		#	v1[i] = sum(self.data[index,self.dictionary['mag']].astype(float)/self.data[index,self.dictionary['err_mag']].astype(float)**2)

		#	for j in xrange(number_of_bins-1):
				
				#import pdb; pdb.set_trace()
		#		index_bins = np.where((self.data[index,self.dictionary[choice[0]]].astype(float)>=self.bins[j]) & (self.data[index,self.dictionary[choice[0]]].astype(float)<self.bins[j+1]))[0]	
				
		#		B[i,j] = sum(1/self.data[index[index_bins],self.dictionary['err_mag']].astype(float)**2)
		#	print i/float(number_of_stars)
					
		#for j in xrange(number_of_bins-1):

		#	index_bins = np.where((self.data[:,self.dictionary[choice[0]]].astype(float)>=self.bins[j]) & (self.data[:,self.dictionary[choice[0]]].astype(float)<self.bins[j+1]))[0]
		#	D[j,j] = sum(1/self.data[index_bins,self.dictionary['err_mag']].astype(float)**2)
		
		#	v2[j] = sum(self.data[index_bins,self.dictionary['mag']].astype(float)/self.data[index_bins,self.dictionary['err_mag']].astype(float)**2)

		A=self.A
		B=self.B
		D=self.D
		v1=self.v1
		v2=self.v2


		Invert_A=np.copy(A)
		for i in xrange(len(A)):

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
		self.x1=np.dot(Invert_A,v1)-np.dot(Invert_A,np.dot(B,x2))
