#!/usr/bin/env python

### This is an example on how works RoboNoise and how you should feed it.
### Two datasets, one linked to OB130446, see Bachelet 2015.
### The other one is a LCOGT dataset for OB141185 planetary event.


# Load standard python modules
import numpy as np
import matplotlib.pyplot as plt
import time
import collections

# Load RoboNoise
import RoboNoise


start = time.time()

# Choose the dataset you want to study. Uncomment it.
data=np.loadtxt('OB141185_lightcurves_coja.txt',dtype='string')
#data=np.loadtxt('Auckland_parameters.txt',dtype='string')
print "Data success load in",time.time()-start,'s'

# Choose the according dictionary you have to pass to the solver. Same order as previously. Dico is the french abbreviation of dictionnary for people interested.
dico = {'stars' : 0, 'frames':1, 'time' : 2 , 'mag' : 14, 'err_mag' : 15,'exposure' : 16,'airmass' : -1,'seeing':18,'background':17,'CCD_X':21,'CCD_Y':22,'phot_scale_factor' :19 }
#dico = {'stars' : 0, 'time' : 2 , 'mag' : 3, 'err_mag' : 4, 'exposure' : 5 , 'airmass' :6,'background' :7, 'seeing' :8,'phot_scale_factor' :9,'CCD_X' :10,'CCD_Y' :11,'frames':12}

# Load the dataset and dictionary for the solver
Solver = RoboNoise.RedNoiseSolver(data,dico)

# Clean the dataset
Solver.clean_bad_data()

# Clean the stars you don't want. Same order as preivously.
Solver.clean_bad_stars(['lc_00325.189_00321.049_t'])
#Solver.clean_bad_stars(['lc_00201.135_00199.462_t'])

# Clean faint star in your dataset. Here we set the faintest to 22 mag.
Solver.clean_magnitude_data(22)

# Choose the quantity you can define regarding what you have in the dataset. For example, if you just have airmass, just put ['airmass']. Same order as previously
#choice=['airmass','exposure','seeing','background','CCD_X','CCD_Y','phot_scale_factor','frames']
choice=['airmass','CCD_X','CCD_Y','exposure','background','seeing','time','phot_scale_factor','frames']

# Define the quantities
Solver.define_continuous_quantities(choice)

Solver.CCD_fit_degree=3

# What do you want to fit. For example, if you want 'airmass' and 'seeing', just put ['airmass','seeing']. Here we want to fit the airmass :
choice=['airmass']

############LEAVE THIS BIT IN FOR DAN TO WRITE OUT THE CLEANED DATA THAT ARE BEING USED FOR TESTING PURPOSES##############
#with open('Dan.Data.OB141185.txt', mode='w') as rfile:
#    for item in Solver.data:
#        line = ''
#        for col in item:
#            line = line + str(col) + ' '
#        rfile.write(line + "\n")

### Python Lesson for Mr Bramich :)
#np.savetxt('Dan.Data.OB130446.txt',Solver.data,fmt='%s')

##########################################################################################################################

# Construct the Bramich and Freudling 2012 matrices.
Solver.construct_continuous_matrices(choice)

# Last step, solve the equations!
Solver.solve()
	


# Now you have solved the equation. As defined in Bramich and Freudling 2012, Solver.x1 is an array containing the "true" magnitudes of the stars (who passed all the cleaning steps).
# Solver.x2 give you the model coefficients estimation, ordering in the same order as quantities. See RoboNoise module for more details.



# We make here some plot for the purpose. We plot the first star magnitude measurement and the model in red vs time. Let's see what we have :

# Plot the star 0 measurements.
index=np.where(Solver.data[:,dico['stars']]==Solver.data[0,dico['stars']])[0]
#plt.errorbar(Solver.data[index,dico['time']].astype(float)-2450000.0,Solver.data[index,dico['mag']].astype(float),yerr=Solver.data[index,dico['err_mag']].astype(float),fmt='.k')

# Construc the model

model=Solver.x1[0]
count=0
for i in choice :
	quantities = Solver.find_model_quantities(i).T

	if quantities.ndim == 1 :
		model += quantities[index]*Solver.x2[count]
		count += 1
	else :

		for j in Solver.find_model_quantities(i).T:

			model += j[index]*Solver.x2[count]
			count += 1
fig=plt.figure()
plt.errorbar(Solver.data[index,dico['time']].astype(float)-2450000.0,Solver.data[index,dico['mag']].astype(float),yerr=Solver.data[index,dico['err_mag']].astype(float),fmt='.k')
plt.plot(Solver.data[index,dico['time']].astype(float)-2450000.0,model,'r',lw=2)
plt.title(Solver.data[0,dico['stars']]+': m = '+str(Solver.x1[0])+' '+str(Solver.x2[0])+'*'+choice[0])
plt.gca().invert_yaxis()
plt.show()
import pdb; pdb.set_trace()
#fig.savefig('../Test_Results/OB141185_'+choice[0],format='png')
#np.savetxt('../Test_Results/OB14185_'+choice[0]+'.txt',np.r_[Solver.x1,Solver.x2].T)

