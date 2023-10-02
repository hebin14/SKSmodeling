/********************************************************
*	Show SAC data max. and min amplitude withing specified time window
*	Usage:
*		lsac2 t1 t2 sac_files ...
*	Modified by Zhigang Peng, Tue Apr 17 17:29:23 PDT 2001
*	By adding abs to the max amplitude
********************************************************/

#include <stdio.h>
#include <math.h>
#include "sac.h"
float absf(float a){
    float b=(a>0)?a:-a;
    return b;
}
int main(int argc, char **argv) {
  SACHEAD	hd;
  int		i,j,n,n1,n2;
  float		*ar=NULL;
  float		t1, t2, am, t, max;

  if (argc < 4) {
     fprintf(stderr, "Usage: lsac_minmax t1 t2 sac_files ...\n");
     return -1;
  }

  sscanf(argv[1],"%f",&t1);
  sscanf(argv[2],"%f",&t2);
  for (i=3;i<argc;i++) {
     if ((ar = read_sac(argv[i],&hd)) == NULL) continue;
     n1= (int) ((t1-hd.b)/hd.delta);if(n1<1) n1=1;
     n2= (int) ((t2-hd.b)/hd.delta);if(n2>hd.npts-2) n2=hd.npts-2;
     if (n1>n2) {
        fprintf(stderr,"no time window for %s\n",argv[i]);
	    continue;
     }
     max=absf(ar[n1]);
     for(j=n1;j<n2;j++) {
        if (absf(ar[j])>max) max = absf(ar[j]);
     }
     printf("%e\n", max);
  }

  return 0;
}
