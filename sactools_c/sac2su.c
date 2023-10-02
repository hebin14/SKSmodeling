/***************************************************************
*	SAC binary files to (seismic unix) su format
*	Usage: sac2su sacfiles gx=gx gy=gy f1=f1 dt=dt ns=ns >out.file
*	gx,gy,f1,dt,ns are integrals, and dt's unit is ns
*       Modified from Lupei's code sac2col
*       Zhigang peng, 10/17/00 13:16:53
*       Bin He, 2023/02/07
***************************************************************/

#include <stdio.h>
#include <stdlib.h>
#include "sac.h"
#include "segy.h"
int main(int argc, char **argv) {
  int		i,j,gx,gy,f1,dt,ns;
  float		*data;
  SACHEAD	hd;
  segy          suhead;
  char     outfilename[80]="";
  if ( argc < 2 ) {
     fprintf(stderr, "Usage: %s sac_files ...\n",argv[0]);
     return -1;
  }
  if ( (data = read_sac(argv[1], &hd)) == NULL ) {
     return -1;
  }
  f1=hd.b;
  dt=hd.delta*1000000;
  ns=hd.npts; 
  sscanf(argv[2],"%s",&outfilename);
  
  printf("filename=%s\n",outfilename);
  printf("ns=%d,dt=%d,sizeof_data=%d,sizeof_segy=%d\n",ns,dt,sizeof(data),sizeof(segy));
  suhead.f1=f1;
  suhead.ns=ns;
  suhead.gx=hd.stlo; 
  suhead.gy=hd.stla;
  suhead.sx=hd.evlo;
  suhead.sy=hd.evla;
  suhead.dt=dt; 
  FILE*fp=fopen(outfilename,"wb");
  fwrite(&suhead,sizeof(segy),1,fp);
  fwrite(data,sizeof(float),ns,fp);
  fclose(fp);

  free(data);

  return 0;

}
