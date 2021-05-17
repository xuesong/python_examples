from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np

x = np.linspace(0,2*np.pi,5000)
plt.plot(x,np.cos(76*x)+np.cos(93*x))


plt.show()