/********************************************************
*       Identify whether SAC data are zeros according to depmin,depmen,depmax
*	Usage:
*		sac_zero  sac_files ...
*	Written by  Kai Wang, 
*	Initial coding: Sat Feb 20 13:13:51 PDT 2019
********************************************************/

#include <stdio.h>
#include <math.h>
#include "sac.h"

int main(int argc, char **argv) {
  SACHEAD	hd;
  int		i,is_zero;
  float		*ar;
  float		min,mean,max;

  if (argc < 2) {
     fprintf(stderr, "Usage: %s sac_files ...\n\
  Identify whether SAC data are zeros according to depmin,depmen,depmax\n",argv[0]);
     return -1;
  }

  for (i=1;i<argc;i++) {

     if ((ar = read_sac(argv[i],&hd)) == NULL) continue;
     min=hd.depmin;
     max=hd.depmax;
     mean=hd.depmen;
     if (fabs(min)<1.e-18 && fabs(max)<1.e-18 && fabs(mean)<1.e-18) {
       is_zero=1;
     }
     else {
       is_zero=0;
     }
     //printf("%s %10.2e %10.2e %10.2e\n", argv[i],fabs(min),fabs(mean),fabs(max));
     printf("%s %d\n",argv[i],is_zero);
  }

  return 0;
}
