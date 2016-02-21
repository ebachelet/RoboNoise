import numpy as np
import RoboNoise
import matplotlib.pyplot as plt

data=np.loadtxt('Auckland_parameters.txt',dtype='string')

Solver = RoboNoise.RedNoiseSolver(data)
Solver.clean_bad_data()
Solver.clean_bad_stars(['lc_00201.135_00199.462_t'])
Solver.clean_magnitude_data(20)
choice=2
Solver.define_bins(choice,0.0)
Solver.solver(choice)
plt.subplot(211)
plt.scatter(Solver.bins[:-1],Solver.x2)
plt.xlabel('Time')
plt.ylabel('Z_Time')

choice=6
Solver.define_bins(choice,20.0)
Solver.solver(choice)
plt.subplot(212)
plt.scatter(Solver.bins[:-1],Solver.x2)
plt.xlabel('Airmass')
plt.ylabel('Z_Airmass')
plt.show()
import pdb; pdb.set_trace()
