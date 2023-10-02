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
  SACHEAD	hd, *hd0;
  int		i,n1;
  float		*ar,*src;
  float		t1;
  char*          inf[64],outf[64];

  if (argc < 4) {
     fprintf(stderr, "Usage: %s t1 saci saco \n\
  Shift SAC data by a time\n",argv[0]);
     return -1;
  }

  sscanf(argv[1],"%f",&t1);
  sprintf(inf,"%s",argv[2]);
  sprintf(outf,"%s",argv[3]);
  //printf("input file: %s\n",inf);
  //printf("output file: %s\n",outf);
  //if ((ar = read_sac(argv[i],&hd)) == NULL) return -1;

  ar = read_sac(inf,&hd);
  src=(float *)malloc(hd.npts*sizeof(float));
  n1= (int) (t1/hd.delta);
  for (i=0;i<hd.npts;i++){
     if ((i+n1)<0 || (i+n1)>hd.npts){
       src[i]=0;
     }
     else {
       src[i]=ar[i+n1];
     }
  }

    hd0=(SACHEAD *)malloc(sizeof(SACHEAD));
    assert(src != NULL && hd0 != NULL);
    memcpy(hd0, &hd, sizeof(SACHEAD));

  write_sac(outf,*hd0, src);
  return 0;
}
