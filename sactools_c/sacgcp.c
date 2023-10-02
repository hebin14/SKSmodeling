/********************************************************
*	read 1-column data from stdin and write them as
*	evenly spaced SAC data.
*	usage:
*		col2sac sac_file_name delta_t t0
*********************************************************/

#include <stdio.h>
#include <stdlib.h>
#include "sac.h"

int main(int argc, char **argv) {

  SACHEAD hd1,hd2;
  int npts,it;
  float baz,theta2;
  float	*tre,*trn,*trr,*trt;
  

  if (argc < 6) {
      fprintf(stderr, "Usage: %s ecmp.sac ncomp.sac rcomp.sac tcomp.sac baz \n\
      Convert gcp rotation from en to rt at station position.\n",argv[0]);
      return -1;
  }

  if ((tre = read_sac(argv[1],&hd1)) == NULL){
    printf("\ne comp can't read\n"); return 0;
  } 
  if ((trn = read_sac(argv[2],&hd2)) == NULL){
    printf("\nn comp can't read\n"); return 0;
  } 
  if(hd1.npts!=hd2.npts) {
    printf("\ne and n comp have differnt length\n");
    return 0;
  }
  sscanf(argv[5],"%f",&baz);
  npts=hd1.npts;
  trt = (float *) calloc(npts,sizeof(float));
  trr = (float *) calloc(npts,sizeof(float));
  memset(trt,0.,sizeof(float)*npts);
  memset(trr,0.,sizeof(float)*npts);
  theta2=baz-180;
  for(it=0;it<npts;it++){
    trt[it]=cos(theta2/180.0*3.1415926)*tre[it]-sin(theta2/180.0*3.1415926)*trn[it];
    trr[it]=sin(theta2/180.0*3.1415926)*tre[it]+cos(theta2/180.0*3.1415926)*trn[it];
  }
  write_sac(argv[3],hd1,trt);
  write_sac(argv[4],hd2,trr);
}
