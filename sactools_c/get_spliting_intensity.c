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
  int		i,nw,ntaper,nwb,nwe;
  float		*tcomp,*rcomp,*window,*wtcomp,*wrcomp;

  float		win_te,win_tb,delta,water_level=1.0e-20,si,norm,spliti;
  char   ftcomp[128],frcomp[128],foutrf[128];

  if (argc < 5) {
     fprintf(stderr, "Usage: %s sactcomp sacrcomp win_tb,win_te \n\
      to get receiver function using in frequency domain\n",argv[0]);
     return -1;
  }
  sprintf(ftcomp,"%s",argv[1]);
  sprintf(frcomp,"%s",argv[2]);
  sscanf(argv[3],"%f",&win_tb);
  sscanf(argv[4],"%f",&win_te);
  
  
  tcomp = read_sac(ftcomp,&hd);
  rcomp = read_sac(frcomp,&hd);
  delta=hd.delta;
  nwb=floor((win_tb-hd.b)/delta);
  nwe=floor((win_te-hd.b)/delta);
  if(nwb<0)nwb=0;
  if(nwe>hd.npts)nwe=hd.npts;
  nw=nwe-nwb+1;
  ntaper=nw/10;
  window=(float*)malloc(nw*(sizeof(float)));
  for(i=0;i<ntaper;i++)window[i]=sin(i*1.0/ntaper*3.1415926/2.0);
  for(i=ntaper;i<nw-ntaper-1;i++)window[i]=1.0;
  for(i=nw-ntaper;i<nw;i++)window[i]=sin((nw-1.-i)/ntaper*3.1415926/2.0);
  
  
  wtcomp=(float*)malloc(nw*(sizeof(float)));
  wrcomp=(float*)malloc(nw*(sizeof(float)));
  for(i=nwb;i<nwe;i++){
    wtcomp[i-nwb]=tcomp[i]*window[i-nwb];
    wrcomp[i-nwb]=(rcomp[i+1]-rcomp[i-1])*window[i-nwb]/2.0/hd.delta;
  }
  norm=0.0;spliti=0.0;
  for(i=0;i<nw;i++){
    norm+=wrcomp[i]*wrcomp[i];
    spliti+=wrcomp[i]*wtcomp[i];
  }
  printf("%f %f %f\n",hd.dist,hd.baz,spliti/norm);
  free(wtcomp);free(wrcomp);free(window);free(tcomp);free(rcomp);
  return 0;
}
