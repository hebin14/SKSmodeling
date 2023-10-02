#BinHe
from netCDF4 import Dataset
import numpy as np
import math
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import  make_axes_locatable
from scipy.interpolate import RegularGridInterpolator as rgi
from scipy import interpolate
import vel2C21
print("===================================")
def vp_vs(vs):
    vp=0.9409 + 2.0947*(vs) - 0.8206*(vs**2) + 0.2683*(vs**3) - 0.0251*(vs**4)
    return vp
def rho_vp(vp):
    rho=1.6612*(vp) - 0.4721*(vp**2) + 0.0671*(vp**3) - 0.0043*(vp**4) + .000106*(vp**5)
    return rho


filep = open('vel.dat', 'r')
Lines = filep.readlines()
  
count = 0
for line in Lines:
    count += 1
    #print("Line{}: {}".format(count, line.strip()))
xx0 = np.zeros(count)
yy0 = np.zeros(count)
zz0 = np.zeros(count)
vs0 = np.zeros(count)
vp0 = np.zeros(count)
rho0 = np.zeros(count)

iz=0
for line in Lines:
    xx0[iz]=float(line.split()[0])
    yy0[iz]=float(line.split()[1])
    zz0[iz]=float(line.split()[2])
    vp0[iz]=float(line.split()[3])
    vs0[iz]=float(line.split()[4])
    rho0[iz]=rho_vp(vp0[iz])
    iz += 1
print('longitude range:',np.min(xx0),np.max(xx0))
print('latitude  range:',np.min(yy0),np.max(yy0))
print('zz0       range:',np.min(zz0),np.max(zz0))
print('vp0       range:',np.min(vp0),np.max(vp0))
print('vs0       range:',np.min(vs0),np.max(vs0))
print('rho0      range:',np.min(rho0),np.max(rho0))

xbeg=140.0
xend=142.0
ybeg=38.75
yend=40.75

zbeg=-5.0
zend=300

num_in_region=0
for iz in range(count):
    if(xx0[iz]>=xbeg and xx0[iz]<=xend and yy0[iz]>=ybeg and yy0[iz]<=yend and zz0[iz]>=zbeg and zz0[iz]<=zend):
        num_in_region += 1
print(num_in_region,count,num_in_region/count*100.0)

xx = np.zeros(num_in_region)
yy = np.zeros(num_in_region)
zz = np.zeros(num_in_region)
vsv = np.zeros(num_in_region)
vpv = np.zeros(num_in_region)
rho = np.zeros(num_in_region)
num_in_region=0
for iz in range(count):
    if(xx0[iz]>=xbeg and xx0[iz]<=xend and yy0[iz]>=ybeg and yy0[iz]<=yend and zz0[iz]>=zbeg and zz0[iz]<=zend):
        xx[num_in_region]=xx0[iz]
        yy[num_in_region]=yy0[iz]
        zz[num_in_region]=zz0[iz]
        vsv[num_in_region]=vs0[iz]
        vpv[num_in_region]=vp0[iz]
        rho[num_in_region]=rho0[iz]
        num_in_region +=1
print("original data range:")
print("X min/max",np.min(xx0),np.max(xx0))
print("Y min/max",np.min(yy0),np.max(yy0))
print("Z min/max",np.min(zz0),np.max(zz0))
print("data range for tomo:")
print("X min/max",np.min(xx),np.max(xx))
print("Y min/max",np.min(yy),np.max(yy))
print("Z min/max",np.min(zz),np.max(zz))
####to see if the dataset is regular
nz=0
for iz in range(num_in_region):
    if(xx[iz]==xx[0] and yy[iz]==yy[0]):
        nz+=1
nx=0
for iz in range(num_in_region):
    if(yy[iz]==yy[0] and zz[iz] == zz[0]):
        nx+=1
ny=0
for iz in range(num_in_region):
    if(xx[iz]==xx[0] and zz[iz]==zz[0]):
        ny+=1
print('size of nx,ny,nz:',nx,ny,nz)

raw_xx=np.zeros(nx)
raw_yy=np.zeros(ny)
raw_zz=np.zeros(nz)
nz=0
for iz in range(num_in_region):
    if(xx[iz]==xx[0] and yy[iz]==yy[0]):
        raw_zz[nz]=zz[iz]
        nz+=1
nx=0
for iz in range(num_in_region):
    if(yy[iz]==yy[0] and zz[iz] == zz[0]):
        raw_xx[nx]=xx[iz]
        nx+=1
ny=0
for iz in range(num_in_region):
    if(xx[iz]==xx[0] and zz[iz]==zz[0]):
        raw_yy[ny]=yy[iz]
        ny+=1
vsv3D = np.zeros(shape=(nx,ny,nz),dtype='float')
vpv3D = np.zeros(shape=(nx,ny,nz),dtype='float')
rho3D = np.zeros(shape=(nx,ny,nz),dtype='float')
# only z direction needs to interp
for iz in range(nz):
    for ix in range(nx):
        for iy in range(ny):
            ik = iz * nx * ny + ix * ny + iy
            vsv3D[ix,iy,iz] = vsv[ik]
            vpv3D[ix,iy,iz] = vpv[ik]
            rho3D[ix,iy,iz] = rho[ik]
nzz=73
new_zz=np.linspace(zbeg,zend,nzz)
new_vsv=np.zeros(nzz)
new_vpv=np.zeros(nzz)
new_rho=np.zeros(nzz)
# interp for every x,y point
raw_vsv=np.zeros(nz)
raw_vpv=np.zeros(nz)
raw_rho=np.zeros(nz)

new_vsv3D = np.zeros(shape=(nx,ny,nzz),dtype='float')
new_vpv3D = np.zeros(shape=(nx,ny,nzz),dtype='float')
new_rho3D = np.zeros(shape=(nx,ny,nzz),dtype='float')
print(new_zz,raw_zz)
for ix in range(nx):
    for iy in range(ny):
        for iz in range(nz):
            raw_vsv[iz] = vsv3D[ix,iy,iz]
            raw_vpv[iz] = vpv3D[ix,iy,iz]
            raw_rho[iz] = rho3D[ix,iy,iz]
        frho=interpolate.interp1d(raw_zz,raw_rho)
        fvpv=interpolate.interp1d(raw_zz,raw_vpv)
        fvsv=interpolate.interp1d(raw_zz,raw_vsv)
        new_rho=frho(new_zz);new_vpv=fvpv(new_zz);new_vsv=fvsv(new_zz)
        for iz in range(nzz):
            new_vsv3D[ix,iy,iz]=new_vsv[iz]
            new_vpv3D[ix,iy,iz]=new_vpv[iz]
            new_rho3D[ix,iy,iz]=new_rho[iz]
###compre xz,yz and xy profiles for doulbe checking
import math

vsvxz=np.zeros(shape=(nx,nz))
vpvxz=np.zeros(shape=(nx,nz))
rhoxz=np.zeros(shape=(nx,nz))

new_vsvxz=np.zeros(shape=(nx,nzz))
new_vpvxz=np.zeros(shape=(nx,nzz))
new_rhoxz=np.zeros(shape=(nx,nzz))

iy=math.floor(ny/2)
vsvxz[:,:]=vsv3D[:,iy,:]
vpvxz[:,:]=vpv3D[:,iy,:]
rhoxz[:,:]=rho3D[:,iy,:]
new_vsvxz[:,:]=new_vsv3D[:,iy,:]
new_vpvxz[:,:]=new_vpv3D[:,iy,:]
new_rhoxz[:,:]=new_rho3D[:,iy,:]

fig,axs=plt.subplots(2,3,constrained_layout=True)
fig.set_size_inches(w=12,h=6)
im=axs[0][0].imshow(vsvxz.T,extent=[xbeg,xend,zend,zbeg],interpolation='none',aspect='auto',cmap='jet');fig.colorbar(im)
axs[0][0].set_ylabel('depth(km)'); axs[0][0].set_xlabel('longitude(deg)') ;axs[0][0].set_title('Vsv (irregular zdepth)');#axs[0][0].invert_yaxis()
im=axs[0][1].imshow(vpvxz.T,extent=[xbeg,xend,zend,zbeg],interpolation='none',aspect='auto',cmap='jet');fig.colorbar(im)
axs[0][1].set_xlabel('longitude(deg)') ;axs[0][1].set_title('Vpv');#axs[0][1].invert_yaxis()
im=axs[0][2].imshow(rhoxz.T,extent=[xbeg,xend,zend,zbeg],interpolation='none',aspect='auto',cmap='jet');fig.colorbar(im)
axs[0][2].set_xlabel('longitude(deg)') ;axs[0][2].set_title('Rho');#axs[0][0].invert_yaxis()

im=axs[1][0].imshow(new_vsvxz.T,extent=[xbeg,xend,zend,zbeg],interpolation='none',aspect='auto',cmap='jet');fig.colorbar(im)
axs[1][0].set_ylabel('depth(km)'); axs[1][0].set_xlabel('longitude(deg)') ;axs[1][0].set_title('Vsv');#axs[0][0].invert_yaxis()
im=axs[1][1].imshow(new_vpvxz.T,extent=[xbeg,xend,zend,zbeg],interpolation='none',aspect='auto',cmap='jet');fig.colorbar(im)
axs[1][1].set_xlabel('longitude(deg)') ;axs[1][1].set_title('Vpv');#axs[0][1].invert_yaxis()
im=axs[1][2].imshow(new_rhoxz.T,extent=[xbeg,xend,zend,zbeg],interpolation='none',aspect='auto',cmap='jet');fig.colorbar(im)
axs[1][2].set_xlabel('longitude(deg)') ;axs[1][2].set_title('Rho');#axs[0][0].invert_yaxis()

plt.savefig("frofile_xz.jpg")

vsvyz=np.zeros(shape=(ny,nz))
vpvyz=np.zeros(shape=(ny,nz))
rhoyz=np.zeros(shape=(ny,nz))

new_vsvyz=np.zeros(shape=(ny,nzz))
new_vpvyz=np.zeros(shape=(ny,nzz))
new_rhoyz=np.zeros(shape=(ny,nzz))

ix=math.floor(nx/2)
vsvyz[:,:]=vsv3D[ix,:,:]
vpvyz[:,:]=vpv3D[ix,:,:]
rhoyz[:,:]=rho3D[ix,:,:]
new_vsvyz[:,:]=new_vsv3D[ix,:,:]
new_vpvyz[:,:]=new_vpv3D[ix,:,:]
new_rhoyz[:,:]=new_rho3D[ix,:,:]

fig,axs=plt.subplots(2,3,constrained_layout=True)
fig.set_size_inches(w=12,h=6)
im=axs[0][0].imshow(vsvyz.T,extent=[xbeg,xend,zend,zbeg],interpolation='none',aspect='auto',cmap='jet');fig.colorbar(im)
axs[0][0].set_ylabel('depth(km)') ;axs[0][0].set_title('Vsv');#axs[0][0].invert_yaxis()
im=axs[0][1].imshow(vpvyz.T,extent=[xbeg,xend,zend,zbeg],interpolation='none',aspect='auto',cmap='jet');fig.colorbar(im)
axs[0][1].set_title('Vpv');#axs[1][1].invert_yaxis()
im=axs[0][2].imshow(rhoyz.T,extent=[xbeg,xend,zend,zbeg],interpolation='none',aspect='auto',cmap='jet');fig.colorbar(im)
axs[0][2].set_title('Rho');#axs[1][2].invert_yaxis()

im=axs[1][0].imshow(new_vsvyz.T,extent=[xbeg,xend,zend,zbeg],interpolation='none',aspect='auto',cmap='jet');fig.colorbar(im)
axs[1][0].set_ylabel('depth(km)'); axs[1][0].set_xlabel('Latitude(deg)')
im=axs[1][1].imshow(new_vpvyz.T,extent=[xbeg,xend,zend,zbeg],interpolation='none',aspect='auto',cmap='jet');fig.colorbar(im)
axs[1][1].set_xlabel('Latitude(deg)')
im=axs[1][2].imshow(new_rhoyz.T,extent=[xbeg,xend,zend,zbeg],interpolation='none',aspect='auto',cmap='jet');fig.colorbar(im)
axs[1][2].set_xlabel('Latitude(deg)')
plt.savefig("frofile_yz.jpg")


vsvxy=np.zeros(shape=(nx,ny))
vpvxy=np.zeros(shape=(nx,ny))
rhoxy=np.zeros(shape=(nx,ny))

new_vsvxy=np.zeros(shape=(nx,ny))
new_vpvxy=np.zeros(shape=(nx,ny))
new_rhoxy=np.zeros(shape=(nx,ny))

dep=30.0
for iz in range(nz):
    if(np.abs(raw_zz[iz]-dep)<3.0):
        vsvxy[:,:]=vsv3D[:,:,iz]
        vpvxy[:,:]=vpv3D[:,:,iz]
        rhoxy[:,:]=rho3D[:,:,iz]

for iz in range(nzz):
    if(np.abs(new_zz[iz]-dep)<3.0):
        new_vsvxy[:,:]=new_vsv3D[:,:,iz]
        new_vpvxy[:,:]=new_vpv3D[:,:,iz]
        new_rhoxy[:,:]=new_rho3D[:,:,iz]

fig,axs=plt.subplots(2,3,constrained_layout=True)
fig.set_size_inches(w=12,h=6)
im=axs[0][0].imshow(vsvxy.T,extent=[xbeg,xend,ybeg,yend],interpolation='none',aspect='auto',cmap='jet');fig.colorbar(im)
axs[0][0].set_ylabel('Latitude(deg)') ;axs[0][0].set_title('Vsv dep=%d'%(dep))
im=axs[0][1].imshow(vpvxy.T,extent=[xbeg,xend,ybeg,yend],interpolation='none',aspect='auto',cmap='jet');fig.colorbar(im)
axs[0][1].set_title('Vpv')
im=axs[0][2].imshow(rhoxy.T,extent=[xbeg,xend,ybeg,yend],interpolation='none',aspect='auto',cmap='jet');fig.colorbar(im)
axs[0][2].set_title('Rho')

im=axs[1][0].imshow(new_vsvxy.T,extent=[xbeg,xend,ybeg,yend],interpolation='none',aspect='auto',cmap='jet');fig.colorbar(im)
axs[1][0].set_ylabel('Latitude(deg)'); axs[1][0].set_xlabel('Longitude(deg)')
im=axs[1][1].imshow(new_vpvxy.T,extent=[xbeg,xend,ybeg,yend],interpolation='none',aspect='auto',cmap='jet');fig.colorbar(im)
axs[1][1].set_xlabel('Longitude(deg)')
im=axs[1][2].imshow(new_rhoxy.T,extent=[xbeg,xend,ybeg,yend],interpolation='none',aspect='auto',cmap='jet');fig.colorbar(im)
axs[1][2].set_xlabel('Longitude(deg)')
plt.savefig("frofile_xy.jpg")

spacing_x=raw_xx[1]-raw_xx[0]
spacing_y=raw_yy[1]-raw_yy[0]
spacing_z=new_zz[1]-new_zz[0]

dsigmah=10;dsigmaz=5
sigmax=(dsigmah/np.abs(spacing_x)/111.9)+1
sigmay=(dsigmah/np.abs(spacing_y)/111.9)+1
sigmaz=(dsigmah/np.abs(spacing_z))

from scipy.ndimage import gaussian_filter
print('smoothing model with spacing=',spacing_x,spacing_y,spacing_z)
print('smoothing the model with sigmaxyz=',sigmax,sigmay,sigmaz)
new_vsv3D=gaussian_filter(new_vsv3D, sigma=[sigmax,sigmay,sigmaz])
new_vpv3D=gaussian_filter(new_vpv3D, sigma=[sigmax,sigmay,sigmaz])
new_rho3D=gaussian_filter(new_rho3D, sigma=[sigmax,sigmay,sigmaz])

vsvxz=np.zeros(shape=(nx,nz))
vpvxz=np.zeros(shape=(nx,nz))
rhoxz=np.zeros(shape=(nx,nz))

new_vsvxz=np.zeros(shape=(nx,nzz))
new_vpvxz=np.zeros(shape=(nx,nzz))
new_rhoxz=np.zeros(shape=(nx,nzz))

iy=math.floor(ny/2)
vsvxz[:,:]=vsv3D[:,iy,:]
vpvxz[:,:]=vpv3D[:,iy,:]
rhoxz[:,:]=rho3D[:,iy,:]
new_vsvxz[:,:]=new_vsv3D[:,iy,:]
new_vpvxz[:,:]=new_vpv3D[:,iy,:]
new_rhoxz[:,:]=new_rho3D[:,iy,:]

fig,axs=plt.subplots(2,3,constrained_layout=True)
fig.set_size_inches(w=12,h=6)
im=axs[0][0].imshow(vsvxz.T,extent=[xbeg,xend,zend,zbeg],interpolation='none',aspect='auto',cmap='jet');fig.colorbar(im)
axs[0][0].set_ylabel('depth(km)'); axs[0][0].set_xlabel('longitude(deg)') ;axs[0][0].set_title('Vsv (irregular zdepth)');#axs[0][0].invert_yaxis()
im=axs[0][1].imshow(vpvxz.T,extent=[xbeg,xend,zend,zbeg],interpolation='none',aspect='auto',cmap='jet');fig.colorbar(im)
axs[0][1].set_xlabel('longitude(deg)') ;axs[0][1].set_title('Vpv');#axs[0][1].invert_yaxis()
im=axs[0][2].imshow(rhoxz.T,extent=[xbeg,xend,zend,zbeg],interpolation='none',aspect='auto',cmap='jet');fig.colorbar(im)
axs[0][2].set_xlabel('longitude(deg)') ;axs[0][2].set_title('Rho');#axs[0][0].invert_yaxis()

im=axs[1][0].imshow(new_vsvxz.T,extent=[xbeg,xend,zend,zbeg],interpolation='none',aspect='auto',cmap='jet');fig.colorbar(im)
axs[1][0].set_ylabel('depth(km)'); axs[1][0].set_xlabel('longitude(deg)') ;axs[1][0].set_title('Vsv');#axs[0][0].invert_yaxis()
im=axs[1][1].imshow(new_vpvxz.T,extent=[xbeg,xend,zend,zbeg],interpolation='none',aspect='auto',cmap='jet');fig.colorbar(im)
axs[1][1].set_xlabel('longitude(deg)') ;axs[1][1].set_title('Vpv');#axs[0][1].invert_yaxis()
im=axs[1][2].imshow(new_rhoxz.T,extent=[xbeg,xend,zend,zbeg],interpolation='none',aspect='auto',cmap='jet');fig.colorbar(im)
axs[1][2].set_xlabel('longitude(deg)') ;axs[1][2].set_title('Rho');#axs[0][0].invert_yaxis()

plt.savefig("frofile_sxz.jpg")

vsvyz=np.zeros(shape=(ny,nz))
vpvyz=np.zeros(shape=(ny,nz))
rhoyz=np.zeros(shape=(ny,nz))

new_vsvyz=np.zeros(shape=(ny,nzz))
new_vpvyz=np.zeros(shape=(ny,nzz))
new_rhoyz=np.zeros(shape=(ny,nzz))

ix=math.floor(nx/2)
vsvyz[:,:]=vsv3D[ix,:,:]
vpvyz[:,:]=vpv3D[ix,:,:]
rhoyz[:,:]=rho3D[ix,:,:]
new_vsvyz[:,:]=new_vsv3D[ix,:,:]
new_vpvyz[:,:]=new_vpv3D[ix,:,:]
new_rhoyz[:,:]=new_rho3D[ix,:,:]

fig,axs=plt.subplots(2,3,constrained_layout=True)
fig.set_size_inches(w=12,h=6)
im=axs[0][0].imshow(vsvyz.T,extent=[xbeg,xend,zend,zbeg],interpolation='none',aspect='auto',cmap='jet');fig.colorbar(im)
axs[0][0].set_ylabel('depth(km)') ;axs[0][0].set_title('Vsv');#axs[0][0].invert_yaxis()
im=axs[0][1].imshow(vpvyz.T,extent=[xbeg,xend,zend,zbeg],interpolation='none',aspect='auto',cmap='jet');fig.colorbar(im)
axs[0][1].set_title('Vpv');#axs[1][1].invert_yaxis()
im=axs[0][2].imshow(rhoyz.T,extent=[xbeg,xend,zend,zbeg],interpolation='none',aspect='auto',cmap='jet');fig.colorbar(im)
axs[0][2].set_title('Rho');#axs[1][2].invert_yaxis()

im=axs[1][0].imshow(new_vsvyz.T,extent=[xbeg,xend,zend,zbeg],interpolation='none',aspect='auto',cmap='jet');fig.colorbar(im)
axs[1][0].set_ylabel('depth(km)'); axs[1][0].set_xlabel('Latitude(deg)')
im=axs[1][1].imshow(new_vpvyz.T,extent=[xbeg,xend,zend,zbeg],interpolation='none',aspect='auto',cmap='jet');fig.colorbar(im)
axs[1][1].set_xlabel('Latitude(deg)')
im=axs[1][2].imshow(new_rhoyz.T,extent=[xbeg,xend,zend,zbeg],interpolation='none',aspect='auto',cmap='jet');fig.colorbar(im)
axs[1][2].set_xlabel('Latitude(deg)')
plt.savefig("frofile_syz.jpg")


vsvxy=np.zeros(shape=(nx,ny))
vpvxy=np.zeros(shape=(nx,ny))
rhoxy=np.zeros(shape=(nx,ny))

new_vsvxy=np.zeros(shape=(nx,ny))
new_vpvxy=np.zeros(shape=(nx,ny))
new_rhoxy=np.zeros(shape=(nx,ny))

dep=30.0
for iz in range(nz):
    if(np.abs(raw_zz[iz]-dep)<3.0):
        vsvxy[:,:]=vsv3D[:,:,iz]
        vpvxy[:,:]=vpv3D[:,:,iz]
        rhoxy[:,:]=rho3D[:,:,iz]

for iz in range(nzz):
    if(np.abs(new_zz[iz]-dep)<3.0):
        new_vsvxy[:,:]=new_vsv3D[:,:,iz]
        new_vpvxy[:,:]=new_vpv3D[:,:,iz]
        new_rhoxy[:,:]=new_rho3D[:,:,iz]

fig,axs=plt.subplots(2,3,constrained_layout=True)
fig.set_size_inches(w=12,h=6)
im=axs[0][0].imshow(vsvxy.T,extent=[xbeg,xend,ybeg,yend],interpolation='none',aspect='auto',cmap='jet');fig.colorbar(im)
axs[0][0].set_ylabel('Latitude(deg)') ;axs[0][0].set_title('Vsv')
im=axs[0][1].imshow(vpvxy.T,extent=[xbeg,xend,ybeg,yend],interpolation='none',aspect='auto',cmap='jet');fig.colorbar(im)
axs[0][1].set_title('Vpv')
im=axs[0][2].imshow(rhoxy.T,extent=[xbeg,xend,ybeg,yend],interpolation='none',aspect='auto',cmap='jet');fig.colorbar(im)
axs[0][2].set_title('Rho')

im=axs[1][0].imshow(new_vsvxy.T,extent=[xbeg,xend,ybeg,yend],interpolation='none',aspect='auto',cmap='jet');fig.colorbar(im)
axs[1][0].set_ylabel('Latitude(deg)'); axs[1][0].set_xlabel('Longitude(deg)')
im=axs[1][1].imshow(new_vpvxy.T,extent=[xbeg,xend,ybeg,yend],interpolation='none',aspect='auto',cmap='jet');fig.colorbar(im)
axs[1][1].set_xlabel('Longitude(deg)')
im=axs[1][2].imshow(new_rhoxy.T,extent=[xbeg,xend,ybeg,yend],interpolation='none',aspect='auto',cmap='jet');fig.colorbar(im)
axs[1][2].set_xlabel('Longitude(deg)')
plt.savefig("frofile_sxy.jpg")

new_vph3D = new_vpv3D*1.0
new_vsh3D = new_vsv3D*1.0
new_vsv3D=new_vsv3D*1000
new_vpv3D=new_vpv3D*1000
new_rho3D=new_rho3D*1000
new_vsh3D=new_vsh3D*1000
new_vph3D=new_vph3D*1000

strength_ani=np.zeros(shape=(nx,ny,nzz),dtype=float)
angle_ani  =np.zeros(shape=(nx,ny,nzz),dtype=float)
Gs =np.zeros(shape=(nx,ny,nzz),dtype=float)
Gc =np.zeros(shape=(nx,ny,nzz),dtype=float)
GsoverL =np.zeros(shape=(nx,ny,nzz),dtype=float)
GcoverL =np.zeros(shape=(nx,ny,nzz),dtype=float)
LL      =np.zeros(shape=(nx,ny,nzz),dtype=float)

angle1=85
perc1=0.05

angle2=-30
perc2=0.03

angle3=-85
perc3=0.02

slab_line1=np.zeros(nx);slab_line2=np.zeros(nx)
slab_line1=90 + (40.-90.)/((raw_xx[-1]-raw_xx[0]))*(raw_xx-raw_xx[0])
slab_line2=slab_line1+100.0


for iz in range(nzz):
    for iy in range(ny):
        for ix in range(nx):
            if(new_zz[iz]<=slab_line1[ix]):
                angle_ani[ix,iy,iz] = angle1 
                strength_ani[ix,iy,iz] = perc1
            elif(new_zz[iz]<=slab_line2[ix]):
                angle_ani[ix,iy,iz] = angle2 
                strength_ani[ix,iy,iz] = perc2
            elif(new_zz[iz]<=240.0):
                angle_ani[ix,iy,iz] = angle3 
                strength_ani[ix,iy,iz] = perc3
##anisotropy


LL= new_vsv3D * new_vsv3D * new_rho3D
G0overL = strength_ani+1.0e-6
GcoverL = G0overL * np.cos(2*angle_ani/180.0*np.pi)
GsoverL = G0overL * np.sin(2*angle_ani/180.0*np.pi)
Gc = GcoverL * LL
Gs = GsoverL * LL

# profiles
iy = int(ny/2)-20
prof_vsv=np.zeros(shape=(nx,nzz),dtype=float)
prof_vsh=np.zeros(shape=(nx,nzz),dtype=float)
prof_vpv=np.zeros(shape=(nx,nzz),dtype=float)
prof_vph=np.zeros(shape=(nx,nzz),dtype=float)
prof_Gs=np.zeros(shape=(nx,nzz),dtype=float)
prof_Gc=np.zeros(shape=(nx,nzz),dtype=float)
prof_rho=np.zeros(shape=(nx,nzz),dtype=float)
prof_angle=np.zeros(shape=(nx,nzz),dtype=float)
prof_perc=np.zeros(shape=(nx,nzz),dtype=float)
for ix in range(nx):
    for iz in range(nzz):
        prof_vsv[ix,iz]=new_vsv3D[ix,iy,iz]
        prof_vsh[ix,iz]=new_vsh3D[ix,iy,iz]
        prof_vpv[ix,iz]=new_vpv3D[ix,iy,iz]
        prof_vph[ix,iz]=new_vph3D[ix,iy,iz]
        prof_rho[ix,iz]=new_rho3D[ix,iy,iz]
        prof_Gs[ix,iz] =Gs[ix,iy,iz]/LL[ix,iy,iz]
        prof_Gc[ix,iz] =Gc[ix,iy,iz]/LL[ix,iy,iz]
        # prof_angle[ix,iz] = angle_ani[ix,iy,iz]
        # prof_perc[ix,iz]  = strength_ani[ix,iy,iz]
        # have to use atan2, it is importrant
        if(ix==10):
            print('ix,iz,',prof_Gs[ix,iz],prof_Gc[ix,iz],prof_Gs[ix,iz]/prof_Gc[ix,iz])
        prof_angle[ix,iz] = np.arctan2(prof_Gs[ix,iz],prof_Gc[ix,iz])/np.pi*90.
        prof_perc[ix,iz]  = np.sqrt(Gs[ix,iy,iz]**2+Gc[ix,iy,iz]**2)/LL[ix,iy,iz]


fig,axs=plt.subplots(2,4,constrained_layout=True)
fig.set_size_inches(w=12,h=6)
im=axs[0][0].imshow(prof_vpv.T,extent=[xbeg,xend,zend,zbeg],interpolation='none',aspect='auto',cmap='jet');fig.colorbar(im)
axs[0][0].set_xlabel('Latitude(deg)');axs[0][0].set_ylabel('Depth (km)') ;axs[0][0].set_title('Vpv dep=%d'%(dep))
im=axs[0][1].imshow(prof_vsv.T,extent=[xbeg,xend,zend,zbeg],interpolation='none',aspect='auto',cmap='jet');fig.colorbar(im)
axs[0][1].set_xlabel('Latitude(deg)');axs[0][1].set_title('Vsv')
im=axs[0][2].imshow(prof_Gc.T,extent=[xbeg,xend,zend,zbeg],interpolation='none',aspect='auto',cmap='jet',vmin=-0.05,vmax=0.05);fig.colorbar(im)
axs[0][2].set_xlabel('Latitude(deg)');axs[0][2].set_title('Gc/LL')
im=axs[0][3].imshow(prof_angle.T,extent=[xbeg,xend,zend,zbeg],interpolation='none',aspect='auto',cmap='jet',vmin=-90,vmax=90);fig.colorbar(im)
axs[0][3].set_xlabel('Latitude(deg)');axs[0][3].set_title('angle')

im=axs[1][0].imshow(prof_vph.T,extent=[xbeg,xend,zend,zbeg],interpolation='none',aspect='auto',cmap='jet');fig.colorbar(im)
axs[1][0].set_xlabel('Latitude(deg)');axs[1][0].set_ylabel('Depth (km)') ;axs[1][0].set_title('Vph')
im=axs[1][1].imshow(prof_vsh.T,extent=[xbeg,xend,zend,zbeg],interpolation='none',aspect='auto',cmap='jet');fig.colorbar(im)
axs[1][1].set_xlabel('Latitude(deg)');axs[1][1].set_title('Vsh')
im=axs[1][2].imshow(prof_Gs.T,extent=[xbeg,xend,zend,zbeg],interpolation='none',aspect='auto',cmap='jet',vmin=-0.05,vmax=0.05);fig.colorbar(im)
axs[1][2].set_xlabel('Latitude(deg)');axs[1][2].set_title('Gs/LL')
im=axs[1][3].imshow(prof_perc.T,extent=[xbeg,xend,zend,zbeg],interpolation='none',aspect='auto',cmap='jet',vmin=0,vmax=0.05);fig.colorbar(im)
axs[1][3].set_xlabel('Latitude(deg)');axs[1][3].set_title('strength')

plt.savefig("anijapan.jpg")
print("======================")




#################################################
######pay attentation to the z coordinate########
#################################################


raw_xx = raw_xx
raw_yy = raw_yy
new_zz = new_zz*-1000
vsvmin=np.min(new_vsv3D)
vpvmin=np.min(new_vpv3D)
rhomin=np.min(new_rho3D)
vsvmax=np.max(new_vsv3D)
vpvmax=np.max(new_vpv3D)
rhomax=np.max(new_rho3D)
##writing the tomography file
spacing_x=raw_xx[1]-raw_xx[0]
spacing_y=raw_yy[1]-raw_yy[0]
spacing_z=new_zz[1]-new_zz[0]

fo = open("tomography_C21_check.dat", "w+") # Name of the file it has to be set in the Par_file
print ("Name of the file: ", fo.name)
fo.write("#------------------------\n")
fo.write("# Sample tomographic file,vpv,vsv,rho,vph,vsh,Gc,Gs\n")
fo.write("#------------------------\n")
fo.write("#orig_x orig_y orig_z end_x end_y end_z\n")
fo.write("%f %f %f %f %f %f\n" % (raw_xx[0],raw_yy[0],new_zz[0],raw_xx[-1],raw_yy[-1],new_zz[-1]))
fo.write("#spacing_x spacing_y spacing_z\n")
fo.write("%f %f %f\n" % (spacing_x,spacing_y,spacing_z))
fo.write("#nx ny nz\n")
fo.write("%d %d %d\n" % (nx,ny,nzz))
fo.write("#vpmin vpmax vsmin vsmax rhomin rhomax\n")
fo.write("%f %f %f %f %f %f\n" % (vpvmin,vpvmax,vsvmin,vsvmax,rhomin,rhomax))
for iz in np.arange(nzz):
    for iy in np.arange(ny):
        for ix in np.arange(nx):
            animodel = vel2C21.Animodel(new_vpv3D[ix,iy,iz],new_vsv3D[ix,iy,iz],new_rho3D[ix,iy,iz],new_vph3D[ix,iy,iz],new_vsh3D[ix,iy,iz],\
                                        Gc[ix,iy,iz],Gs[ix,iy,iz])
            animodel.get_C21()
            if(ix==int(nx/2) and iy==int(ny/2) and np.mod(iz,3)==0):
                print('remember that, Gc=(d55-d44)/2, Gs=-d45 rather than Gc=(C55-C44)/2, Gs=-C45')
                print('the angle you defined is counter-clock from source in global coodrinate')
                print('depth Gc and Gs',new_zz[iz],Gc[ix,iy,iz],Gs[ix,iy,iz],'C44 and C55',animodel.c44,animodel.c55,'(C55-C44)/2.0',(animodel.c55-animodel.c44)/2.0)
                animodel.check_model_input()
                animodel.check_model_output()  
            fo.write("%f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f\n" \
            % (float(raw_xx[ix]),float(raw_yy[iy]),float(new_zz[iz]),\
            animodel.c11,animodel.c12,animodel.c13,animodel.c14,animodel.c15,animodel.c16,\
            animodel.c22,animodel.c23,animodel.c24,animodel.c25,animodel.c26,animodel.c33,\
            animodel.c34,animodel.c35,animodel.c36,animodel.c44,animodel.c45,animodel.c46,\
            animodel.c55,animodel.c56,animodel.c66,new_rho3D[ix,iy,iz]))
fo.close()
raw_vpv1d=np.zeros(nzz)
raw_vsv1d=np.zeros(nzz)
raw_rho1d=np.zeros(nzz)
for iz in np.arange(nzz):
    for iy in np.arange(ny):
        for ix in np.arange(nx):
            raw_vpv1d[iz]=raw_vpv1d[iz]+new_vpv3D[ix,iy,iz]/nx/ny
            raw_vsv1d[iz]=raw_vsv1d[iz]+new_vsv3D[ix,iy,iz]/nx/ny
            raw_rho1d[iz]=raw_rho1d[iz]+new_rho3D[ix,iy,iz]/nx/ny

zend=-300000.0;zbeg=0;num=11;spacing_z=(zend-zbeg)/(num-1)
zzz=np.zeros(num)
for iz in np.arange(num):
    zzz[iz]=zbeg+spacing_z*iz

rho1d=np.zeros(num);vsv1d=np.zeros(num);vpv1d=np.zeros(num)
frho=interpolate.interp1d(new_zz,raw_rho1d)
fvpv=interpolate.interp1d(new_zz,raw_vpv1d)
fvsv=interpolate.interp1d(new_zz,raw_vsv1d)
rho1d=frho(zzz);vpv1d=fvpv(zzz);vsv1d=fvsv(zzz)

fo = open("FK1d.xyz", "w+") # Name of the file it has to be set in the Par_file
fo.write("NLAYER         %d\n" % (num))
for iz in np.arange(np.size(zzz)):
    fo.write("LAYER %d %f %f %f %d\n" % (iz+1,float(rho1d[iz]),float(vpv1d[iz]),float(vsv1d[iz]),float(zzz[iz])))
fo.close()

plt.figure()
plt.plot(new_zz,raw_vsv1d,'b',zzz,vsv1d,'r')
plt.savefig('interp1d.jpg')


fo = open("tomography_vpvz3D.xyz", "w+") # Name of the file it has to be set in the Par_file
print ("Name of the file: ", fo.name)
fo.write("#------------------------\n")
fo.write("# Sample tomographic file,vpv,vsv,rho,vph,vsh,Gc,Gs\n")
fo.write("#------------------------\n")
fo.write("#orig_x orig_y orig_z end_x end_y end_z\n")
fo.write("%f %f %f %f %f %f\n" % (raw_xx[0],raw_yy[0],new_zz[0],raw_xx[-1],raw_yy[-1],new_zz[-1]))
fo.write("#spacing_x spacing_y spacing_z\n")
fo.write("%f %f %f\n" % (spacing_x,spacing_y,spacing_z))
fo.write("#nx ny nz\n")
fo.write("%d %d %d\n" % (nx,ny,nzz))
fo.write("#vpmin vpmax vsmin vsmax rhomin rhomax\n")
fo.write("%f %f %f %f %f %f\n" % (vpvmin,vpvmax,vsvmin,vsvmax,rhomin,rhomax))
for iz in np.arange(nzz):
    for iy in np.arange(ny):
        for ix in np.arange(nx):
            fo.write("%f %f %f %f %f %f\n" % (float(raw_xx[ix]),float(raw_yy[iy]),float(new_zz[iz]),float(new_vpv3D[ix,iy,iz]),float(new_vsv3D[ix,iy,iz]),float(new_rho3D[ix,iy,iz])))
fo.close()

