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
vsh=np.zeros(shape=(nz,ny,nx),dtype=float)
vph=np.zeros(shape=(nz,ny,nx),dtype=float)
rho=np.zeros(shape=(nz,ny,nx),dtype=float)

strength_ani=np.zeros(shape=(nz,ny,nx),dtype=float)
angle_ani  =np.zeros(shape=(nz,ny,nx),dtype=float)
Gs =np.zeros(shape=(nz,ny,nx),dtype=float)
Gc =np.zeros(shape=(nz,ny,nx),dtype=float)
GsoverL =np.zeros(shape=(nz,ny,nx),dtype=float)
GcoverL =np.zeros(shape=(nz,ny,nx),dtype=float)
LL      =np.zeros(shape=(nz,ny,nx),dtype=float)

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

vph = vpv*1.0
vsh = vsv*1.0

angle=0
perc=0.0

for iz in range(nz):
    for iy in range(ny):
        for ix in range(nx):
            if(depth[iz]<-30000. and depth[iz]>-120000.):
                angle_ani[iz,iy,ix] = angle 
                strength_ani[iz,iy,ix] = perc
##anisotropy
LL= vsv * vsv * rho
G0overL = strength_ani
GcoverL = G0overL * np.cos(2*angle_ani/180.0*np.pi)
GsoverL = G0overL * np.sin(2*angle_ani/180.0*np.pi)

Gc = GcoverL * LL
Gs = GsoverL * LL


# profiles
iy = int(ny/2)-20
prof_vsv=np.zeros((nz,nx))
prof_vsh=np.zeros((nz,nx))
prof_vpv=np.zeros((nz,nx))
prof_vph=np.zeros((nz,nx))
prof_Gs=np.zeros((nz,nx))
prof_Gc=np.zeros((nz,nx))
prof_rho=np.zeros((nz,nx))
prof_angle=np.zeros((nz,nx))
prof_perc=np.zeros((nz,nx))
for iz in range(nz):
    for ix in range(nx):
        prof_vsv[iz,ix]=vsv[iz,iy,ix]
        prof_vsh[iz,ix]=vsh[iz,iy,ix]
        prof_vpv[iz,ix]=vpv[iz,iy,ix]
        prof_vph[iz,ix]=vph[iz,iy,ix]
        prof_rho[iz,ix]=rho[iz,iy,ix]
        prof_Gs[iz,ix] =Gs[iz,iy,ix]/LL[iz,iy,ix]
        prof_Gc[iz,ix] =Gc[iz,iy,ix]/LL[iz,iy,ix]
        prof_angle[iz,ix] = np.arctan(Gs[iz,iy,ix]/(Gc[iz,iy,ix]+1.0e-10))/3.14*90.
        prof_perc[iz,ix]  = np.sqrt(Gs[iz,iy,ix]**2+Gc[iz,iy,ix]**2)/LL[iz,iy,ix]

f = plt.figure(figsize=(20,8))
plt.subplot(2,5,1)
plt.imshow(prof_vpv,aspect='auto',extent=[lon_beg,lon_end,dep_end/1000,dep_beg/1000],cmap='jet')
im_ratio = prof_vpv.shape[0]/prof_vpv.shape[1]
plt.colorbar(fraction=0.047*im_ratio);plt.gca().invert_yaxis() 
plt.title("Vpv")                                                                    

plt.subplot(2,5,2)
plt.imshow(prof_vsv,aspect='auto',extent=[lon_beg,lon_end,dep_end/1000,dep_beg/1000],cmap='jet')
plt.colorbar(fraction=0.047*im_ratio) ;plt.gca().invert_yaxis() 
plt.title("Vsv")   

plt.subplot(2,5,3)
plt.imshow(prof_rho,aspect='auto',extent=[lon_beg,lon_end,dep_end/1000,dep_beg/1000],cmap='jet')
plt.colorbar(fraction=0.047*im_ratio) ;plt.gca().invert_yaxis() 
plt.title("Rho")   

plt.subplot(2,5,4)
plt.imshow(prof_Gc,aspect='auto',extent=[lon_beg,lon_end,dep_end/1000,dep_beg/1000],cmap='jet')
plt.colorbar(fraction=0.047*im_ratio) ;plt.gca().invert_yaxis() 
plt.title("Gc/overL")   
plt.subplot(2,5,5)
plt.imshow(prof_Gs,aspect='auto',extent=[lon_beg,lon_end,dep_end/1000,dep_beg/1000],cmap='jet')
plt.colorbar(fraction=0.047*im_ratio) ;plt.gca().invert_yaxis() 
plt.title("Gs/overL") 

plt.subplot(2,5,6)
plt.imshow(prof_vph,aspect='auto',extent=[lon_beg,lon_end,dep_end/1000,dep_beg/1000],cmap='jet')
plt.colorbar(fraction=0.047*im_ratio) ;plt.gca().invert_yaxis() 
plt.title("Vph")   

plt.subplot(2,5,7)
plt.imshow(prof_vsh,aspect='auto',extent=[lon_beg,lon_end,dep_end/1000,dep_beg/1000],cmap='jet')
plt.colorbar(fraction=0.047*im_ratio) ;plt.gca().invert_yaxis() 
plt.title("Vsh")   

plt.subplot(2,5,8)
plt.imshow(prof_angle,aspect='auto',extent=[lon_beg,lon_end,dep_end/1000,dep_beg/1000],cmap='jet')
plt.colorbar(fraction=0.047*im_ratio) ;plt.gca().invert_yaxis() 
plt.title("aniso_angle")   
plt.subplot(2,5,9)
plt.imshow(prof_perc,aspect='auto',extent=[lon_beg,lon_end,dep_end/1000,dep_beg/1000],cmap='jet')
plt.colorbar(fraction=0.047*im_ratio) ;plt.gca().invert_yaxis() 
plt.title("aniso_perturbation") 

plt.tight_layout()
f.savefig("ak135_C21_angle_%2.2f_perc_%2.2f.jpg"%(angle,perc))
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
fo = open("tomography_ak135_C21_angle_%2.2f_perc_%2.2f.dat"%(angle,perc), "w+") # Name of the file it has to be set in the Par_file
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
            animodel = vel2C21.Animodel(vpv[iz,iy,ix],vsv[iz,iy,ix],rho[iz,iy,ix],vph[iz,iy,ix],vsh[iz,iy,ix],\
                                        Gc[iz,iy,ix],Gs[iz,iy,ix])
            animodel.get_C21()
            if(ix==int(nx/2) and iy==int(ny/2) and np.mod(iz,10)==0):
                print('remember that, Gc=(d55-d44)/2, Gs=-d45 rather than Gc=(C55-C44)/2, Gs=-C45')
                print('the angle you defined is counter-clock due source in global coodrinate')
                print('Gc and Gs',Gc[iz,iy,ix],Gs[iz,iy,ix],'C44 and C55',animodel.c44,animodel.c55,'(C55-C44)/2.0',(animodel.c55-animodel.c44)/2.0)
                animodel.check_model_input()
                animodel.check_model_output()
                
            fo.write("%f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f\n" \
            % (float(lonx[ix]),float(laty[iy]),float(depth[iz]),\
            animodel.c11,animodel.c12,animodel.c13,animodel.c14,animodel.c15,animodel.c16,\
            animodel.c22,animodel.c23,animodel.c24,animodel.c25,animodel.c26,animodel.c33,\
            animodel.c34,animodel.c35,animodel.c36,animodel.c44,animodel.c45,animodel.c46,\
            animodel.c55,animodel.c56,animodel.c66,rho[iz,iy,ix]))
fo.close()

