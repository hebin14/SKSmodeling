/********************************************************
*	Calculate signal to noise ratio for SAC data 
*	within specified time window
*	modified from sac_e
*	Usage:
*		sac_e -Ssingal_start_time -Wtime_window sac_files ...
*	Modified from lsac2, by Zhigang Peng, Fri Aug  9 11:13:54 PDT 2002
********************************************************/

#include <stdio.h>
#include <assert.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include "sac.h"
#include "Complex.h"

int main(int argc, char **argv) {
  SACHEAD	hd;
  int		i,j,st1,st2, error,nrdc, p_arr, s_arr;
  float		*trace, align;
  float		twin, sst, nst, ntwin, stwin, signal, signal_max,t_first_arrival;

  error = 0;
  nrdc = -5; /* default, align from begining */
  /* input parameters */
  for (i=1; !error && i < argc; i++) {
    if (argv[i][0] == '-') {
       switch(argv[i][1]) {

       case 'S':
  	 sscanf(&argv[i][2],"%f",&sst);
         break;

       case 'W':
  	 sscanf(&argv[i][2],"%f",&twin);
         break;

       default:
         error = 1;
         break;

       }
    }
  }

  if (argc < 3 || error) {
     fprintf(stderr, "Usage: %s -Ssingal_start_time \n\
  	 -Wtime_window sac_files \n\
  Estimate the first arrival for SAC data \n\
  within specified time window \n",argv[0]);
     return -1;
  }

  for (i=1;i<argc;i++) {
     if (argv[i][0] == '-') continue;
     if ((trace = read_sac(argv[i],&hd)) == NULL ||
	hd.depmax < -12340. || hd.depmin > 1234000000. ) {
           fprintf(stderr,"error opening %s or missing head info\n",argv[i]);
	   continue;
     }

     align = - hd.b;
     st1= (int) (align/hd.delta);if(st1<0) st1=0;
     st2= (int) ((align+sst+twin)/hd.delta);if(st2>hd.npts-2) st2=hd.npts-2;
     if (st1 > st2) {
        fprintf(stderr,"time window for the noise or signal is less than 1 for %s\n",argv[i]);
	continue;
     }else if ((nrdc == -2 && st2>s_arr) || (nrdc == 0 && st1<p_arr)) {
/*       fprintf(stderr,"Alert, signal window including both P and S arrivals %s\n",argv[i]); */
     }
     stwin = st2-st1+1.;
     signal = 0;
     signal_max = hd.depmax;
     for(j=st1;j<st2;j++) trace[j] = abs(trace[j])/abs(signal_max+1.0e-30);
     t_first_arrival = st1*hd.delta+hd.b;
     for(j=st1;j<st2;j++) {
	if(trace[j]>0.2){
		t_first_arrival = hd.b + j* hd.delta;	
		break;
	}		
     }
     printf("%s %f %f %f\n", argv[i],t_first_arrival,sst,sst+twin);
  }

  return 0;
}
