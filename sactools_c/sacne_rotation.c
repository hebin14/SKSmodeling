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
  float az,baz,theta1,theta2;
  float	*tree,*tren,*trne,*trnn,*trrr,*trrt,*trtr,*trtt,*trte,*trtn,*trre,*trrn;
  

  if (argc < 11) {
      fprintf(stderr, "Usage: %s ecmp.sac ncomp.sac rcomp.sac tcomp.sac az baz \n\
      Convert gcp rotation from en to rt at station position.\n",argv[0]);
      return -1;
  }

  if ((tree = read_sac(argv[1],&hd1)) == NULL){
    printf("\nee comp can't read\n"); return 0;
  } 
  if ((tren = read_sac(argv[2],&hd2)) == NULL){
    printf("\nen comp can't read\n"); return 0;
  } 
  if ((trne = read_sac(argv[3],&hd1)) == NULL){
    printf("\nne comp can't read\n"); return 0;
  } 
  if ((trnn = read_sac(argv[4],&hd2)) == NULL){
    printf("\nnn comp can't read\n"); return 0;
  } 
  if(hd1.npts!=hd2.npts) {
    printf("\ne and n comp have differnt length\n");
    return 0;
  }
  sscanf(argv[9],"%f",&az);
  sscanf(argv[10],"%f",&baz);
  npts=hd1.npts;
  trtt = (float *) calloc(npts,sizeof(float));
  trrr = (float *) calloc(npts,sizeof(float));
  trtr = (float *) calloc(npts,sizeof(float));
  trrt = (float *) calloc(npts,sizeof(float));
  memset(trtt,0.,sizeof(float)*npts);
  memset(trtr,0.,sizeof(float)*npts);
  memset(trrr,0.,sizeof(float)*npts);
  memset(trrt,0.,sizeof(float)*npts);
  theta1=az;
  theta2=baz-180;
  trte = (float *) calloc(npts,sizeof(float));
  trtn = (float *) calloc(npts,sizeof(float));
  trre = (float *) calloc(npts,sizeof(float));
  trrn = (float *) calloc(npts,sizeof(float));
  memset(trte,0.,sizeof(float)*npts);
  memset(trtn,0.,sizeof(float)*npts);
  memset(trre,0.,sizeof(float)*npts);
  memset(trrn,0.,sizeof(float)*npts);
  for(it=0;it<npts;it++){
    trte[it]=cos(theta1/180.0*3.1415926)*tree[it]-sin(theta1/180.0*3.1415926)*trne[it];
    trtn[it]=cos(theta1/180.0*3.1415926)*tren[it]-sin(theta1/180.0*3.1415926)*trnn[it];
    trre[it]=sin(theta1/180.0*3.1415926)*tree[it]+cos(theta1/180.0*3.1415926)*trne[it];
    trrn[it]=sin(theta1/180.0*3.1415926)*tren[it]+cos(theta1/180.0*3.1415926)*trnn[it];
  }
  for(it=0;it<npts;it++){
    trtt[it]=cos(theta2/180.0*3.1415926)*trte[it]-sin(theta2/180.0*3.1415926)*trtn[it];
    trtr[it]=sin(theta2/180.0*3.1415926)*trte[it]+cos(theta2/180.0*3.1415926)*trtn[it];

    trrt[it]=cos(theta2/180.0*3.1415926)*trre[it]-sin(theta2/180.0*3.1415926)*trrn[it];
    trrr[it]=sin(theta2/180.0*3.1415926)*trre[it]+cos(theta2/180.0*3.1415926)*trrn[it];
    
  }
  write_sac(argv[5],hd1,trtt);
  write_sac(argv[6],hd1,trtr);
  write_sac(argv[7],hd2,trrt);
  write_sac(argv[8],hd2,trrr);
  free(trtt);free(trrr);free(trrt);free(trtr);
  free(tree);free(tren);free(trnn);free(trne);
  free(trtn);free(trte);free(trrn);free(trre);

}
