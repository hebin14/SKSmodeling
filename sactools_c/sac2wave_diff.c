/***************************************************************
*	Dump SAC binary files to stdout
*	Usage:
*	 sac2col sac_files ...
***************************************************************/

#include <stdio.h>
#include <stdlib.h>
#include "sac.h"

int main(int argc, char **argv) {
  int		i,j;
  float		*data1,*data2;
  SACHEAD	hd1,hd2;

  if ( argc < 3 ) {
     fprintf(stderr, "Usage: %s sac_files ...\n",argv[0]);
     return -1;
  }

  if ( (data1 = read_sac(argv[1], &hd1)) == NULL ) {
    printf("\n sacfile %s read error",argv[1]);
	  return 0;
  }
  if ( (data2 = read_sac(argv[2], &hd2)) == NULL ) {
    printf("\n sacfile %s read error",argv[2]);
	  return 0;
  }
  if(hd1.npts!=hd2.npts){
    printf("\n sacfiles have differnt length");
	  return 0;
  }
	for(j=0;j<hd1.npts;j++)
		printf("%f %e\n",hd1.b+hd1.delta*j,data1[j]-data2[j]);
       
    free(data1);free(data2);
  return 0;
}
