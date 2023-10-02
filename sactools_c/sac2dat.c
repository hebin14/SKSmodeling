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
  float tb,te,stlo,stla,evla,evlo;
  int npts;
  SACHEAD	hd;

  if ( argc < 2 ) {
     fprintf(stderr, "Usage: %s sac_files ...\n",argv[0]);
     return -1;
  }

  for(i=1;i<argc;i++){

       if ( (data = read_sac(argv[i], &hd)) == NULL ) {
	  continue;
       }
       npts=hd.npts;
       tb=hd.b;te=hd.e;
       stla=hd.stla; stlo=hd.stlo;
       evla=hd.evla; evlo=hd.evlo;
       if(-tb!=te){
        printf("\n I need Gab and Gba are equal tb=%f,te=%f\n",tb,te);
       }else{
       	    printf("%f %f\n",evlo,evla);
       	    printf("%f %f\n",stlo,stla);
		    printf("%f %e %e\n",0.,data[(hd.npts-1)/2],-data[(hd.npts-1)/2]);
	  	    for(j=0;j<hd.npts/2;j++)
		        printf("%f %e %e\n",(j+1)*hd.delta,data[(hd.npts-1)/2+j+1],data[(hd.npts-1)/2-j-1]);
       }
       free(data);
  }

  return 0;

}
