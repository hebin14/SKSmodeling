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
  int i,n,max_len_char=128;
  float *tt,*aa,dt,t0;
  SACHEAD hd;
  char	fsemd[max_len_char],fsac[max_len_char],dummy_line[max_len_char];
  FILE*fp=NULL;
  if (argc != 3) {
     fprintf(stderr,"Usage: semd2sac fsemd fsac\n");
     return 1;
  }

  sscanf(argv[1],"%s",&fsemd[0]);
  sscanf(argv[2],"%s",&fsac[0]);
  fp=fopen(fsemd,"r");
  if(fp == NULL) {
    perror("Unable to open file!");
    exit(1);
  }
  i = 0;
  while (fgets(dummy_line,sizeof(dummy_line),fp)) i++;
  fclose(fp);
  n = i;
  tt = (float *) calloc(n,sizeof(float));
  aa = (float *) calloc(n,sizeof(float));
  fp=fopen(fsemd,"r");
  printf("\n fsemd=%s,fsac=%s \n",fsemd,fsac);
  for(i=0;i<n;i++){
    fscanf(fp,"%f %f\n",&tt[i],&aa[i]);
  }
  fclose(fp);
  dt = tt[1] - tt[0];
  t0 = tt[0];
  hd = sachdr(dt,n,t0);
  return write_sac(fsac,hd,aa);
}
