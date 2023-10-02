/********************************************************
*	Calculate SAC data total energy (amplitude^2) withing specified time window
*	and normalize to single data point
*	Usage:
*		sac2aq output sac_files
*	Written by Kai Wang, Fri Feb 25 11:13:54 PDT 2019
********************************************************/

#include <stdio.h>
#include <math.h>
#include "sac.h"

int main(int argc, char **argv) {
  SACHEAD	hd;
  int		i,j;
  float		*ar;
  float         lat,lon,dep;
  int           yr,mon,day,hr,min;
  float         sec,tpre,dt;
  int           nsta;
  FILE          *f;
  

  if (argc < 3) {
     fprintf(stderr, "Usage: %s output_filename sac_files \n\
  Convert sac files to one aq files for the program astack.\n",argv[0]);
     return -1;
  }


  f=fopen(argv[1],"w");
  for (i=2;i<argc;i++) {
     if ((ar = read_sac(argv[i],&hd)) == NULL) continue;
     // read event info from the first sac file
     if (i==2) {
        lat=hd.evla;
        lon=hd.evlo;
        dep=hd.evdp;
        yr=hd.nzyear;
        mon=0;
        day=hd.nzjday;
        hr=hd.nzhour;
        min=hd.nzmin;
        sec=hd.nzsec+0.001*hd.nzmsec;
        fprintf(f,"%d\n",argc-2);
        fprintf(f,"%12.4f  %12.4f  %12.4f\n",lat,lon,dep/1000.);
        fprintf(f,"%5d   %2d    %3d\n",yr,mon,day);
        fprintf(f,"%d   %d  %12.4f    %12.4f\n",hr,min,sec,tpre);
        fprintf(f,"%f P\n",hd.delta);
     }
     tpre=0.;
     fprintf(f,"%d %d %f %.8s\n",1,hd.npts,tpre,hd.kstnm);
     for(j=0;j<hd.npts;j++) {
        fprintf(f,"%e ",ar[j]);
     }
     fprintf(f,"\n");
  }
  fclose(f);

  return 0;
}
