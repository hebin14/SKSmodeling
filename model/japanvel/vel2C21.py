# mapping the velocity models to the C21 tenser for anisotropy modeling for specfem3D # 
# Bin He, 2022-11-17 @UTD, hebin14@mails.ucas.ac.cn
import numpy as np
class Animodel:
  def __init__(self, vpv,vsv,rho,vph,vsh,Gc,Gs):
        self.vpv = vpv
        self.vsv = vsv
        self.rho = rho
        self.vph = vph
        self.vsh = vsh
        self.Gc  = Gc
        self.Gs  = Gs
        self.c11 = 0; self.c12 = 0; self.c13 = 0; self.c14 = 0; self.c15 = 0; self.c16 = 0
        self.c22 = 0; self.c23 = 0; self.c24 = 0; self.c25 = 0; self.c26 = 0
        self.c33 = 0; self.c34 = 0; self.c35 = 0; self.c36 = 0
        self.c44 = 0; self.c45 = 0; self.c46 = 0
        self.c55 = 0; self.c56 = 0
        self.c66 = 0

  def check_model_input(self):
      print("model input values: vpv %7.3e\t|"%(self.vpv)+"vsv %7.3e\t|"%(self.vsv)+ "rho %7.3e\t|"%(self.rho)+"vph %7.3e\t|"%(self.vph)\
          +"vsh %7.3e\t|"%(self.vsh)+"Gc %7.3e\t|"%(self.Gc)+"Gs %7.3e\t"%(self.Gs))
  
  def get_C21(self):
      eta_aniso = 1.0
      aa = self.rho*self.vph*self.vph
      cc = self.rho*self.vpv*self.vpv
      nn = self.rho*self.vsh*self.vsh
      ll = self.rho*self.vsv*self.vsv
      ff = eta_aniso*(aa - 2.*ll)

      # zeta-independant, these five are for VTI
      A = aa
      C = cc
      AN = nn
      AL = ll
      F = ff

      # zeta-dependant terms
      C1p = 0.0
      C1sv = 0.0
      C1sh = 0.0
      S1p = 0.0
      S1sv = 0.0
      S1sh = 0.0

      # two-zeta dependant terms
      #Gc = 0.0
      #Gs = 0.0

      Bc = 0.0
      Bs = 0.0

      Hc = 0.0
      Hs = 0.0

      # three-zeta dependant terms
      C3 = 0.0
      S3 = 0.0

      # four-zeta dependant terms
      Ec = 0.0
      Es = 0.0

      #----------------- from xueyan --------------#
      # the transverse aniso case
      # Cmn = [A    A-2N  F    0   0   0]
      #       [A-2N   A   F    0   0   0]
      #       [  F    F   C    0   0   0]
      #       [  0    0   0    L   0   0]
      #       [  0    0   0    0   L   0]
      #       [  0    0   0    0   0   N]
      #--------------------------------------------#
      # the transverse aniso case
      # Cmn = [A    A-2N  F    0   0   0]
      #       [A-2N   A   F    0   0   0]
      #       [  F    F   C    0   0   0]
      #       [  0    0   0    Gc  Gs  0]
      #       [  0    0   0    Gs  Gc  0]
      #       [  0    0   0    0   0   N]
      #-------------------------------------------#
      #  unused: fills values with the isotropic model
      #  c11 = rho*vpv*vpv
      #  c12 = rho*(vpv*vpv-2.*vsv*vsv)
      #  c13 = c12
      #  c14 = 0.d0
      #  c15 = 0.d0
      #  c16 = 0.d0
      #  c22 = c11
      #  c23 = c12
      #  c24 = 0.d0
      #  c25 = 0.d0
      #  c26 = 0.d0
      #  c33 = c11
      #  c34 = 0.d0
      #  c35 = 0.d0
      #  c36 = 0.d0
      #  c44 = rho*vsv*vsv
      #  c45 = 0.d0
      #  c46 = 0.d0
      #  c55 = c44
      #  c56 = 0.d0
      #  c66 = c44
      # The mapping from the elastic coefficients to the elastic tensor elements
      # in the local Cartesian coordinate system (classical geographic) used in the
      # global code (1---South, 2---East, 3---up)
      # Always keep the following part when you modify this subroutine
      d11 = A + Ec + Bc                    # same as iso(lamda+2*mu)
      d12 = A - 2.*AN - Ec                 # same as iso(lamda)
      d13 = F + Hc                         # same as iso(lamda)
      d14 = S3 + 2.*S1sh + 2.*S1p          # 0
      d15 = 2.*C1p + C3                    # 0
      d16 = -Bs/2. - Es                    # 0
      d22 = A + Ec - Bc                    # same as iso (lamda+2*mu)
      d23 = F - Hc                         # same as iso (lamda)
      d24 = 2.*S1p - S3                    # 0
      d25 = 2.*C1p - 2.*C1sh - C3          # 0
      d26 = -Bs/2. + Es                    # 0
      d33 = C                              # same as iso (lamda+2*mu)
      d34 = 2.*(S1p - S1sv)                # 0
      d35 = 2.*(C1p - C1sv)                # 0
      d36 = -Hs                            # 0
      d44 = AL - self.Gc                        # differnt from iso, mu - Gc
      d45 = -self.Gs                            # differnt from iso, -Gs
      d46 = C1sh - C3                      # 0.
      d55 = AL + self.Gc                        # differnt from iso, mu + Gc
      d56 = S3 - S1sh                      # 0
      d66 = AN - Ec                        # same as iso (mu)

      # The mapping to the global Cartesian coordinate system used in the code
      # (1---East, 2---North, 3---up)
      self.c11 = d22                            # same as iso(lamda+2*mu)
      self.c12 = d12                            # same as iso(lamda)
      self.c13 = d23                            # same as iso(lamda)
      self.c14 = - d25                          # 0
      self.c15 = d24                            # 0
      self.c16 = - d26                          # 0
      self.c22 = d11                            # same as iso(lamda+2*mu)
      self.c23 = d13                            # same as iso(lamda)
      self.c24 = - d15                          # 0
      self.c25 = d14                            # 0
      self.c26 = - d16                          # 0
      self.c33 = d33                            # same as iso (lamda+2*mu)
      self.c34 = - d35                          # 0
      self.c35 = d34                            # 0
      self.c36 = - d36                          # 0
      self.c44 = d55                            # differnt from iso, mu + Gc
      self.c45 = - d45                          # differnt from iso, Gs
      self.c46 = d56                            # 0
      self.c55 = d44                            # differnt from iso, mu - Gc
      self.c56 = - d46                          # 0
      self.c66 = d66                            # same as iso (mu)
  def check_model_output(self):
      print("model output values: C11 %7.3e\t|"%(self.c11)+"C12 %7.3e\t|"%(self.c12)+ "C13 %7.3e\t|"%(self.c13)+"C14 %7.3e\t|"%(self.c14)\
          +"C15 %7.3e\t|"%(self.c15)+"C16 %7.3e\t|"%(self.c16))
      print("model output values: C22 %7.3e\t|"%(self.c22)+"C23 %7.3e\t|"%(self.c23)+ "C24 %7.3e\t|"%(self.c24)+"C25 %7.3e\t|"%(self.c25)\
          +"C26 %7.3e\t"%(self.c26))
      print("model output values: C33 %7.3e\t|"%(self.c33)+"C34 %7.3e\t|"%(self.c34)+ "C35 %7.3e\t|"%(self.c35)+"C36 %7.3e\t"%(self.c36))
      print("model output values: C44 %7.3e\t|"%(self.c44)+"C45 %7.3e\t|"%(self.c45)+ "C46 %7.3e\t"%(self.c46))
      print("model output values: C55 %7.3e\t|"%(self.c55)+"C56 %7.3e\t"%(self.c56))
      print("model output values: C66 %7.3e\t"%(self.c66))
