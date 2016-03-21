import numpy as np
import RoboNoise
import matplotlib.pyplot as plt

#data=np.loadtxt('OB141185_lightcurves_coja.txt',dtype='string')
data=np.loadtxt('Auckland_parameters.txt',dtype='string')



#dico = {'stars' : 0, 'time' : 1 , 'mag' : 13, 'err_mag' : 14,'exposure' : 15,'airmass' : 6}
dico = {'stars' : 0, 'time' : 2 , 'mag' : 3, 'err_mag' : 4, 'exposure' : 5 , 'airmass' :6}
Solver = RoboNoise.RedNoiseSolver(data,dico)
Solver.clean_bad_data()
#Solver.clean_bad_stars(['lc_00325.189_00321.049_t'])
Solver.clean_bad_stars(['lc_00201.135_00199.462_t'])
Solver.clean_magnitude_data(22)
choice=['time']
Solver.construct_matrices(choice)
#Solver.define_bins(choice,0.0)
Solver.solver(choice)
plt.subplot(311)
plt.scatter(Solver.quantities.time-2450000,Solver.x2)
mag1=Solver.x1
plt.xlabel('Time')
plt.ylabel('Z_Time')
plt.gca().invert_yaxis()

choice=['airmass']
Solver.construct_matrices(choice)
#Solver.define_bins(choice,0.0)
Solver.solver(choice)
plt.subplot(312)
plt.scatter(Solver.quantities.airmass,Solver.x2)
plt.xlabel('Airmass')
plt.ylabel('Z_Airmass')
plt.gca().invert_yaxis()
choice=['exposure']
Solver.construct_matrices(choice)
#Solver.define_bins(choice,0.0)
Solver.solver(choice)
plt.subplot(313)
plt.scatter(Solver.quantities.exposure,Solver.x2)
plt.xlabel('Airmass')
plt.ylabel('Z_Airmass')
plt.gca().invert_yaxis()
plt.figure()
choice=['time','airmass','exposure']
Solver.construct_matrices(choice)
Solver.solver(choice)
plt.subplot(311)
plt.scatter(Solver.quantities.time-2450000,Solver.x2[:len(Solver.quantities.time)])

plt.xlabel('time')
plt.ylabel('Z_time')
plt.gca().invert_yaxis()

plt.subplot(312)
plt.scatter(Solver.quantities.airmass,Solver.x2[len(Solver.quantities.time):len(Solver.quantities.time)+len(Solver.quantities.airmass)])

plt.xlabel('airmass')
plt.ylabel('Z_airmass')
plt.gca().invert_yaxis()
plt.subplot(313)
plt.scatter(Solver.quantities.exposure,Solver.x2[len(Solver.quantities.time)+len(Solver.quantities.airmass):])

plt.xlabel('exposure')
plt.ylabel('Z_exposure')
plt.gca().invert_yaxis()

plt.show()
import pdb; pdb.set_trace()
