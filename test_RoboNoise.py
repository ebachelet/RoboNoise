import numpy as np
import RoboNoise
import matplotlib.pyplot as plt

#data=np.loadtxt('OB141185_lightcurves_coja.txt',dtype='string')
data=np.loadtxt('Auckland_parameters.txt',dtype='string')

#data[:,3] = data[:,3].astype(float)+data[:,6].astype(float)*10-10

#dico = {'stars' : 0, 'time' : 1 , 'mag' : 13, 'err_mag' : 14,'exposure' : 15,'airmass' : 6,'frames':2}
dico = {'stars' : 0, 'time' : 2 , 'mag' : 3, 'err_mag' : 4, 'exposure' : 5 , 'airmass' :6,'background' :7, 'seeing' :8,'CCD_X' :10,'CCD_Y' :11,'frames':12}
Solver = RoboNoise.RedNoiseSolver(data,dico)
Solver.clean_bad_data()
#Solver.clean_bad_stars(['lc_00325.189_00321.049_t'])
Solver.clean_bad_stars(['lc_00201.135_00199.462_t'])
Solver.clean_magnitude_data(22)
choice=['airmass','exposure','seeing','background']
#choice=['airmass','CCD_X','CCD_Y','exposure','background','seeing','time']
Solver.define_continuous_quantities(choice)
choice=['exposure','background']
Solver.construct_continuous_matrices(choice)
Solver.solve()
print Solver.x1[0],Solver.x2[0]
import pdb; pdb.set_trace()

model = Solver.x1[0]
strings='Mag : '+str(Solver.x1[0])+' ; '
for i in xrange(len(choice)) :
	model = model+Solver.data[:109,dico[choice[i]]].astype(float)*Solver.x2[i]
	strings = strings + choice[i]+ ' : '+ str(Solver.x2[i])+'*x ; '
plt.errorbar(Solver.data[:109,2].astype(float)-2450000.0,Solver.data[:109,dico['mag']].astype(float),yerr=Solver.data[:109,dico['err_mag']].astype(float),fmt='.k')
plt.gca().invert_yaxis()
plt.plot(Solver.data[:109,2].astype(float)-2450000.0,model,'r',lw=2)
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

