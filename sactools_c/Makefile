CFLAGS = -O
CC=icc
#
SAC = col2sac gsact lsac0 lsac lsac1 lsac2 sac2col sac_ave sac_zero sac2aq \
	sac_shift sacdump sacdump_slice sac_e saclst sac_me sac_snr sacStack \
	lsac_minmax lsacmax distaz distbaz ndistbaz sac_first_arrival sac2su sac2dat get_spliting_intensity \
	zrt2psvsh
	

all: $(SAC) $(SAC2)
	rm *.o

$(SAC): %:%.o sacio.o fft.o Complex.o
	${CC} -o $@ $@.o sacio.o fft.o Complex.o -lm
