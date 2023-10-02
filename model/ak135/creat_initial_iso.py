#BinHe
import numpy as np
import math
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import  make_axes_locatable
from scipy.interpolate import RegularGridInterpolator as rgi
import matplotlib.cm as cm
import vel2C21
print("======================")
print("Hello World!!")
def vp_vs(vs):
    vp=0.9409 + 2.0947*(vs) - 0.8206*(vs**2) + 0.2683*(vs**3) - 0.0251*(vs**4)
    return vp
def rho_vp(vp):
    rho=1.6612*(vp) - 0.4721*(vp**2) + 0.0671*(vp**3) - 0.0043*(vp**4) + .000106*(vp**5)
    return rho
#step 1 choose data range
lonmin=140.0
lonmax=142.0
latmin=38.75
latmax=40.75
lat_beg=latmin
lat_end=latmax
lon_beg=lonmin
lon_end=lonmax
dep_beg=0.0
dep_end=-200000.0
nx=41
ny=41
nz=41

lonx=np.zeros(nx)
laty=np.zeros(ny)
depth=np.zeros(nz)

for ix in range(nx):
    lonx[ix] = lon_beg + ix * (lon_end - lon_beg) /( nx - 1.) 
for iy in range(ny):
    laty[iy] = lat_beg + iy * (lat_end - lat_beg) /( ny - 1.) 
for iz in range(nz):
    depth[iz] = dep_beg + iz * (dep_end - dep_beg) /( nz - 1.) 

vsv=np.zeros(shape=(nz,ny,nx),dtype=float)
vpv=np.zeros(shape=(nz,ny,nx),dtype=float)
rho=np.zeros(shape=(nz,ny,nx),dtype=float)

# 0.000      5.8000      3.4600     2.7200
# 20.000      5.8000      3.4600      2.7200
# 20.000      6.5000      3.8500      2.9200
# 35.000      6.5000      3.8500      2.9200
# 35.000      8.0400      4.4800      3.3198
# 77.500      8.0450      4.4900      3.3455
# 120.000      8.0500      4.5000      3.3713
# 165.000      8.1750      4.5090      3.3985
# 210.000      8.3000      4.5180      3.4258
# 210.000      8.3000      4.5230      3.4258
# 260.000      8.4825      4.6090      3.4561
# 310.000      8.6650      4.6960      3.4864
# 360.000      8.8475      4.7830      3.5167
# 410.000      9.0300      4.8700      3.5470
# 410.000      9.3600      5.0800      3.7557
for iz in range(nz):
    for iy in range(ny):
        for ix in range(nx):
            if(depth[iz]<-120000.):
                vsv[iz,iy,ix] = 4518.00
                vpv[iz,iy,ix] = 8300.00
                rho[iz,iy,ix] = 3425.80
            elif(depth[iz]<-30000.):
                vsv[iz,iy,ix] = 4490.00
                vpv[iz,iy,ix] = 8040.00
                rho[iz,iy,ix] = 3319.80
            else:
                vsv[iz,iy,ix] = 3460.00
                vpv[iz,iy,ix] = 5800.00
                rho[iz,iy,ix] = 2720.70

# profiles
iy = int(ny/2)-20
prof_vsv=np.zeros((nz,nx))
prof_vpv=np.zeros((nz,nx))
prof_rho=np.zeros((nz,nx))
for iz in range(nz):
    for ix in range(nx):
        prof_vsv[iz,ix]=vsv[iz,iy,ix]
        prof_vpv[iz,ix]=vpv[iz,iy,ix]
        prof_rho[iz,ix]=rho[iz,iy,ix]
f = plt.figure(figsize=(12,4))
plt.subplot(1,3,1)
plt.imshow(prof_vpv,aspect='auto',extent=[lon_beg,lon_end,dep_end/1000,dep_beg/1000],cmap='jet')
im_ratio = prof_vpv.shape[0]/prof_vpv.shape[1]
plt.colorbar(fraction=0.047*im_ratio);plt.gca().invert_yaxis() 
plt.title("Vpv") 
plt.ylabel("Depth (km)") 
plt.xlabel("Longitude (deg)")                                                                    

plt.subplot(1,3,2)
plt.imshow(prof_vsv,aspect='auto',extent=[lon_beg,lon_end,dep_end/1000,dep_beg/1000],cmap='jet')
plt.colorbar(fraction=0.047*im_ratio) ;plt.gca().invert_yaxis() 
plt.title("Vsv")   
plt.xlabel("Longitude (deg)") 

plt.subplot(1,3,3)
plt.imshow(prof_rho,aspect='auto',extent=[lon_beg,lon_end,dep_end/1000,dep_beg/1000],cmap='jet')
plt.colorbar(fraction=0.047*im_ratio) ;plt.gca().invert_yaxis() 
plt.title("Rho")   
plt.xlabel("Longitude (deg)") 

plt.tight_layout()
f.savefig("ak135_iso.jpg")
print("======================")



vsmin=np.min(vsv)
vpmin=np.min(vpv)
rhomin=np.min(rho)
vsmax=np.max(vsv)
vpmax=np.max(vpv)
rhomax=np.max(rho)
##writing the tomography file
spacing_x=lonx[1]-lonx[0]
spacing_y=laty[1]-laty[0]
spacing_z=depth[1]-depth[0]
fo = open("tomography_ak135_iso.dat", "w+") # Name of the file it has to be set in the Par_file
print ("Name of the file: ", fo.name)
fo.write("#------------------------\n")
fo.write("# Sample tomographic file,vpv,vsv,rho,vph,vsh,Gc,Gs\n")
fo.write("#------------------------\n")
fo.write("#orig_x orig_y orig_z end_x end_y end_z\n")
fo.write("%f %f %f %f %f %f\n" % (lon_beg,lat_beg,dep_beg,lon_end,lat_end,dep_end))
fo.write("#spacing_x spacing_y spacing_z\n")
fo.write("%f %f %f\n" % (spacing_x,spacing_y,spacing_z))
fo.write("#nx ny nz\n")
fo.write("%d %d %d\n" % (nx,ny,nz))
fo.write("#vpmin vpmax vsmin vsmax rhomin rhomax\n")
fo.write("%f %f %f %f %f %f\n" % (vpmin,vpmax,vsmin,vsmax,rhomin,rhomax))
for iz in np.arange(nz):
    for iy in np.arange(ny):
        for ix in np.arange(nx):
            fo.write("%f %f %f %f %f %f\n" \
            % (float(lonx[ix]),float(laty[iy]),float(depth[iz]),\
            vpv[iz,iy,ix],vsv[iz,iy,ix],rho[iz,iy,ix]))
fo.close()

