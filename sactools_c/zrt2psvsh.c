/********************************************************
*	Shift sac data by a time 
*	Usage:
*		sac_ave t1 t2 sac_files ...
*	Written by Kai Wang, 
*	Initial coding: Sat Feb 18 20:50:51 PDT 2019
********************************************************/

#include <stdio.h>
#include <assert.h>
#include <math.h>
#include "sac.h"


int main(int argc, char **argv) {
  SACHEAD	hd;
  int		i,npts;
  float	*tcomp,*rcomp,*zcomp,*pcomp,*svcomp,*shcomp;
  float	vs,vp,inc_ang,alpha,beta,rayp,qalpha,qbeta;
  float term11,term12,term13,term21,term22,term23,term31,term32,term33;
  char  ftcomp[128],frcomp[128],fzcomp[128],fpcomp[128],fsvcomp[128],fshcomp[128];
   
  if (argc < 10) {
     fprintf(stderr, "Usage: %s saczcomp sactcomp sacrcomp sacpcomp,sacsvcomp,sacshcomp vp vs \n\
      to get receiver function using in frequency domain\n",argv[0]);
     return -1;
  }
  sprintf(fzcomp,"%s",argv[1]);
  sprintf(frcomp,"%s",argv[2]);
  sprintf(ftcomp,"%s",argv[3]);
  sscanf(argv[7],"%f",&vp);
  sscanf(argv[8],"%f",&vs);
  sscanf(argv[9],"%f",&inc_ang);
  
  zcomp = read_sac(fzcomp,&hd);
  rcomp = read_sac(frcomp,&hd);
  tcomp = read_sac(ftcomp,&hd);
  
  npts=hd.npts;
  pcomp=(float*)malloc(npts*(sizeof(float)));
  svcomp=(float*)malloc(npts*(sizeof(float)));
  shcomp=(float*)malloc(npts*(sizeof(float)));
  memset(pcomp,0.,sizeof(float)*npts);
  memset(svcomp,0.,sizeof(float)*npts);
  memset(shcomp,0.,sizeof(float)*npts);

  alpha=vp;beta=vs;rayp=sin(inc_ang/180.0*3.1415926)/beta;
  qalpha=sqrt(1.0/alpha/alpha-rayp*rayp);
  qbeta=sqrt(1.0/beta/beta-rayp*rayp);
  term11=(beta*beta*rayp*rayp-0.5)/(alpha*qalpha);
  term12=rayp*beta*beta/alpha;
  term13=0.0;
  term21=rayp*beta;
  term22=0.5-beta*beta*rayp*rayp/(beta*qbeta);
  term23=0.0;
  term31=0;
  term32=0;
  term33=0.5;
  for(i=0;i<npts;i++){
    pcomp[i] =term11*zcomp[i]+term12*rcomp[i]+term13*tcomp[i];
    svcomp[i]=term21*zcomp[i]+term22*rcomp[i]+term23*tcomp[i];
    shcomp[i]=term31*zcomp[i]+term32*rcomp[i]+term33*tcomp[i];
  }
  write_sac(argv[4],hd, pcomp);
  write_sac(argv[5],hd, svcomp);
  write_sac(argv[6],hd, shcomp);
  free(tcomp);free(rcomp);free(zcomp);
  free(pcomp);free(svcomp);free(shcomp);
  return 0;
}
