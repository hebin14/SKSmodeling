import vel2C21
import numpy as np
vsv = 3460.00
vpv = 5800.00
rho = 2720.70

vsh = 3460.00
vph = 5800.00

Gc  = 0
Gs  = 0
angle_ani=0
strength_ani=0.1

LL= vsv * vsv * rho
G0overL = strength_ani
GcoverL = G0overL * np.cos(2*angle_ani/180.0*np.pi)
GsoverL = G0overL * np.sin(2*angle_ani/180.0*np.pi)

Gc = GcoverL * LL
Gs = GsoverL * LL

animodel = vel2C21.Animodel(vpv,vsv,rho,vph,vsh,Gc,Gs)
animodel.check_model_input()
animodel.get_C21()
animodel.check_model_output()