import numpy as np
import matplotlib.pyplot as plt

print(".......")
print('script for cut and creating a topo graphy file with boundayies taper to zero')
filep = open('topo_japan.dat', 'r')
Lines = filep.readlines()
count = 0
for line in Lines:
    count += 1

lonx=np.zeros(count)
laty=np.zeros(count)
topo=np.zeros(count)
iz=0
for line in Lines:
    lonx[iz]=float(line.split(" ")[0])
    laty[iz]=float(line.split(" ")[1])
    topo[iz]=float(line.split(" ")[2])
    iz+=1
xbeg=140.0
xend=142.0
ybeg=38.75
yend=40.75
num_in_region=0
for iz in range(count):
    if(lonx[iz]>=xbeg and lonx[iz]<=xend and laty[iz]>=ybeg and laty[iz]<=yend):
        num_in_region += 1
print(num_in_region,count,num_in_region/count*100.0)

xx = np.zeros(num_in_region)
yy = np.zeros(num_in_region)
zz = np.zeros(num_in_region)
num_in_region=0
for iz in range(count):
    if(lonx[iz]>=xbeg and lonx[iz]<=xend and laty[iz]>=ybeg and laty[iz]<=yend):
      xx[num_in_region]=lonx[iz]
      yy[num_in_region]=laty[iz]
      zz[num_in_region]=topo[iz]
      num_in_region +=1

ny=0
for iz in range(num_in_region):
  if(np.abs(xx[iz]-xx[0])<0.0001):
    ny+=1
nx=0
for iz in range(num_in_region):
  if(np.abs(yy[iz]-yy[0])<0.0001):
    nx+=1
print('study region nx,ny:',nx,ny,num_in_region-nx*ny)

print('study region Lon min/max:',np.min(xx),np.max(xx),np.size(xx))

print('study region Lat min/max:',np.min(yy),np.max(yy),np.size(yy))
topo2d=np.zeros(shape=[nx,ny],dtype=float)
for iy in range(ny):
  for ix in range(nx):
    iyx= iy * nx + ix
    topo2d[ix,iy]=zz[iyx]

ntaper=40
ntaper_beg=8

taper=np.zeros(shape=[nx,ny],dtype=float)


for ix in range(nx):
  for iy in range(ny):
    taper[ix,iy]=1.0

taper1d=np.zeros(shape=[nx,1],dtype=float)
for ix in range(ntaper_beg,ntaper):
  taper1d[ix] = np.sin((ix-ntaper_beg)*1.0/(ntaper-ntaper_beg)*3.14/2.0)
  

##left
for ix in range(ntaper):
  for iy in range(ny):
    taper[ix][iy] *= taper1d[ix]
##right
for ix in range(nx-ntaper+1,nx):
  for iy in range(ny):
    taper[ix][iy] *= taper1d[nx-ix]
##top
for iy in range(ntaper):
  for ix in range(nx):
    taper[ix][iy] *= taper1d[iy]
##bottom
for iy in range(ny-ntaper+1,ny):
  for ix in range(nx):
    taper[ix][iy] *= taper1d[ny-iy]

fig, ax = plt.subplots()
im = ax.imshow(taper.T)
#ax.set_title('')
plt.xlabel('x grid number')
plt.ylabel('y grid number')
fig.colorbar(im, ax=ax, label='taper function')             
plt.savefig("taper.jpg")


topo2d *= taper
fig, ax = plt.subplots()
im = ax.imshow(topo2d.T)
#ax.set_title('')
plt.xlabel('x grid number')
plt.ylabel('y grid number')
fig.colorbar(im, ax=ax, label='Topography (m)')             
plt.savefig("topo.jpg")
fig.colorbar(im, ax=ax, label='Interactive colorbar')

f = open("topo_japan_taper.dat", "w")
for iy in range(ny):
  for ix in range(nx):
    f.write("%f\n"%topo2d[ix,iy])
f.close()
print(".......")
print("very good,finished")
