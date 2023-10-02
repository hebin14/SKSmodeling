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
  float		*data;
  SACHEAD	hd;

  if ( argc < 2 ) {
     fprintf(stderr, "Usage: %s sac_files ...\n",argv[0]);
     return -1;
  }

  for(i=1;i<argc;i++){
    if ( (data = read_sac(argv[i], &hd)) == NULL ) {
	    continue;
    }
	  for(j=0;j<hd.npts;j++)
		  printf("%f %e\n",hd.b+hd.delta*j,data[j]);
       
    free(data);

  }

  return 0;

}
