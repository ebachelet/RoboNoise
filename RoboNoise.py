import numpy as np
import collections
from scipy.optimize import leastsq
class RedNoiseSolver(object):


	def __init__(self, data, dictionary) :

		self.data = data
		self.dictionary = dictionary
		self.model_quantities = collections.namedtuple('Models',[])
		self.ref_star =[]	

	

	def  construct_continuous_matrices(self,choices):

                # Determine the star list
		stars = np.unique(self.data[:,self.dictionary['stars']])
		number_of_stars = len(stars)
		# Determine the frame list
		frames = np.unique(self.data[:,self.dictionary['frames']])
		number_of_frames = len(frames)
		# create quantity to fit
		quantities = self.find_model_quantities(choices[0])
		for i in choices[1:] :
			quantities = np.c_[quantities,self.find_model_quantities(i)]
			
                # MAKE CHECK HERE THAT THERE ARE AT LEAST TWO STARS - MORE ROBUST CODE - AND REPORT AN ERROR MESSAGE IF NOT

		A_diagonal = []
		v1 = []
		count = 0	
		for i in stars :
			index = np.where(self.data[:,self.dictionary['stars']]==i)[0]
			A_diagonal.append(sum(1/self.data[index,self.dictionary['err_mag']].astype(float)**2))
			v1.append(sum(self.data[index,self.dictionary['mag']].astype(float)/self.data[index,self.dictionary['err_mag']].astype(float)**2))
			
				
		# Construct the B sub-matrix
		B=[]
		for i in xrange(number_of_stars):
			
			index = np.where(self.data[:,self.dictionary['stars']]==stars[i])[0]
			line=[]
			if quantities.ndim==1:
					
				line+=[np.sum(quantities[index]*1/self.data[index,self.dictionary['err_mag']].astype(float)**2)]					
			
			else:

				line+=np.sum(quantities[index].T*1/self.data[index,self.dictionary['err_mag']].astype(float)**2,axis=1).tolist()

				
			B.append(line)
				
		B=np.array(B)
		
		# Construct the D matrix and v2 vector
		
		
		D=[]
		v2=[]
		if quantities.ndim==1:
			n_dim = 1
		else:
			n_dim =quantities.shape[1]
		for i in xrange(n_dim)  :
			if n_dim==1:
				quantities_i=quantities
			else :

				quantities_i=quantities[:,i]
			line=[]	
			for j in  xrange(n_dim) :
			
				if n_dim==1:
					quantities_j=quantities
				else :

					quantities_j=quantities[:,j]
				somme = 0
				for k in xrange(number_of_frames) :
						index_i=np.where(self.data[:,self.dictionary['frames']]==frames[k])[0]
						index_j=np.where(self.data[:,self.dictionary['frames']]==frames[k])[0]
						somme += np.sum(quantities_i[index_i]*quantities_j[index_j]/self.data[index_i,self.dictionary['err_mag']].astype(float)**2) 
				line += [somme]
			D.append(line)
			v2.append(np.sum(quantities_i[:]*self.data[:,self.dictionary['mag']].astype(float)/self.data[:,self.dictionary['err_mag']].astype(float)**2)) 
		
		D=np.array(D)
		v2=np.array(v2)

		self.A_diagonal=np.array(A_diagonal)
		self.B=B
		self.D=D
		self.v1=v1
		self.v2=v2

	def find_model_quantities(self,choice) :
		
		if choice == 'seeing' :
			return self.model_seeing() 
		
		if choice == 'airmass' :
			return self.model_airmass() 
		if choice == 'phot_scale_factor' :
			return self.model_phot_scale_factor() 	
		if choice == 'CCD' :
			return self.model_CCD_positions() 
		if choice == 'exposure' :
			return self.model_exposure_time() 
		if choice == 'background' :
			return self.model_background() 

	# definitions of continuous quantities functions. Mainly linear functions for a start.

	def model_airmass(self) :
		# f(x) = a*x
		quantity = self.quantities.airmass
		#quantity = np.c_[quantity,self.quantities.airmass**2]
		#quantity = np.c_[quantity,self.quantities.airmass**3]
		return quantity


	def model_CCD_positions(self) :
		#import pdb; pdb.set_trace()	
		#f(x) = a_i*x**i*y**j	
		
		degree = 2
		offset_CCD = self.quantities.CCD_X
		for i in range(degree+1) :
			for j in range(degree+1) :
			
				if (i+j>degree) | (i+j==0) :	
					pass
				else :

					offset_CCD = np.c_[offset_CCD, self.quantities.CCD_X**(i)*self.quantities.CCD_Y**(j)]

		return offset_CCD[:,1:]
		
	
	def model_exposure_time(self) :
		# f(x) = a*x
		offset_exptime =self.quantities.exposure
		#offset_exptime =np.c_[offset_exptime ,self.quantities.exposure**2]
		return offset_exptime

	def model_seeing(self) :
		# f(x) = a*x
		offset_seeing = self.quantities.seeing
		return offset_seeing
	def model_background(self) :
		# f(x) = a*x
		offset_background = self.quantities.background
		return offset_background

	def model_phot_scale_factor(self) :
		# f(x) = a*x
		offset_phot_scale_factor =self.quantities.phot_scale_factor
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

	def define_continuous_quantities(self,choices):
		
		interest=['airmass','CCD_X','CCD_Y','exposure','background','seeing','time','phot_scale_factor']
		quantities=collections.namedtuple('Quantities',interest)
		for i in interest :

			if i in choices :
				setattr(quantities,i,self.data[:,self.dictionary[i]].astype(float))
			else :

				setattr(quantities,i,np.array([0]*len(self.data)))
		
		self.quantities = quantities

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

	def solve(self) :

		A_diagonal=self.A_diagonal
		B=self.B
		C=self.B.T		
		D=self.D
		v1=self.v1
		v2=self.v2
		
		Invert_A_diagonal=1/A_diagonal	

		
		term1=Invert_A_diagonal[:,None]*B	
		term2=np.dot(C,term1)
		term3=D-term2
		term4=Invert_A_diagonal*v1
		term5=np.dot(C,term4)
		term6 = v2-term5
			
		# inverting matrix, not really efficient 
		#Invert = np.linalg.inv(term3)
		#x2=np.dot(Invert,term6)


		#x2=np.linalg.solve(term3,term6)# solver, not the best
		
		#leastsq solver
		x2=np.linalg.lstsq(term3,term6)[0]
		
		self.x2 = x2
		self.x1=term4-Invert_A_diagonal*np.dot(B,x2)
		
