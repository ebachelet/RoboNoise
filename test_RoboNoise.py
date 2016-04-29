import numpy as np
import RoboNoise
import matplotlib.pyplot as plt
import time

start = time.time()
data=np.loadtxt('OB141185_lightcurves_coja.txt',dtype='string')
#data=np.loadtxt('Auckland_parameters.txt',dtype='string')
print "data success load in",time.time()-start

#data[:,14] = data[:,14].astype(float)+data[:,-1].astype(float)*1
dico = {'stars' : 0, 'frames':1, 'time' : 2 , 'mag' : 14, 'err_mag' : 15,'exposure' : 16,'airmass' : -1,'seeing':18,'background':17,'CCD_X':21,'CCD_Y':22,'phot_scale_factor' :19 }
#dico = {'stars' : 0, 'time' : 2 , 'mag' : 3, 'err_mag' : 4, 'exposure' : 5 , 'airmass' :6,'background' :7, 'seeing' :8,'phot_scale_factor' :9,'CCD_X' :10,'CCD_Y' :11,'frames':12}

Solver = RoboNoise.RedNoiseSolver(data,dico)
Solver.clean_bad_data()
Solver.clean_bad_stars(['lc_00325.189_00321.049_t'])
#Soldata[ver.clean_bad_stars(['lc_00201.135_00199.462_t'])

Solver.clean_magnitude_data(22)
choice=['airmass','exposure','seeing','background','CCD_X','CCD_Y','phot_scale_factor']
#choice=['airmass','CCD_X','CCD_Y','exposure','background','seeing','time']
Solver.define_continuous_quantities(choice)
choice=['airmass']
Solver.construct_continuous_matrices(choice)
Solver.solve()
print Solver.x1[0],Solver.x2[0]
import pdb; pdb.set_trace()

model = Solver.x1[0]
strings='Mag : '+str(Solver.x1[0])+' ; '
for i in xrange(len(choice)) :
	model = model+Solver.data[:148,dico[choice[i]]].astype(float)*Solver.x2[i]
	strings = strings + choice[i]+ ' : '+ str(Solver.x2[i])+'*x ; '
plt.errorbar(Solver.data[:148,2].astype(float)-2450000.0,Solver.data[:148,dico['mag']].astype(float),yerr=Solver.data[:148,dico['err_mag']].astype(float),fmt='.k')
plt.gca().invert_yaxis()
plt.plot(Solver.data[:148,2].astype(float)-2450000.0,model,'r',lw=2)
plt.title(strings)
plt.show()
import pdb; pdb.set_trace()
med_mag=[]
std_mag=[]
med_mag_corrected=[]
std_mag_corrected=[]
for i in np.unique(Solver.data[:,0]) :

	index=np.where(Solver.data[:,0]==i)[0]
 	med_mag.append(np.median(Solver.data[index,3].astype(float)))
	std_mag.append(np.std(Solver.data[index,3].astype(float)))
	med_mag_corrected.append(np.median(Solver.data[index,3].astype(float)-Solver.x2*Solver.data[index,dico[choice[0]]].astype(float)))
	std_mag_corrected.append(np.std(Solver.data[index,3].astype(float)-Solver.x2*Solver.data[index,dico[choice[0]]].astype(float)))

plt.scatter(med_mag,std_mag)
plt.scatter(med_mag,std_mag_corrected,c='r')
plt.show()
import pdb; pdb.set_trace()

