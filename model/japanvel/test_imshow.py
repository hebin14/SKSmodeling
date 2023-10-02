import numpy as np
import math
import matplotlib.pyplot as plt
nx=400
nz=100
xbeg=0
xend=100
zbeg=-200
zend=200
xx=np.linspace(xbeg,xend,nx)
zz=np.linspace(zbeg,zend,nz)
matrix=np.zeros(shape=(nx,nz))

for ix in range(nx):
  for iz in range(nz):
    matrix[ix,iz]=ix+iz
plt.figure

plt.imshow(matrix.T,extent=[xbeg,xend,zend,zbeg],interpolation='none',aspect='auto',cmap='jet',origin='lower')
plt.colorbar()
plt.savefig("test_imshow.jpg")