.SUFFIXES: .cc

CC = /usr/bin/gcc

PATH_ALGLIB = /home/nick/HDD/Work/GNU/ALGLIB/mpfr/out
PATH_GMP = /home/nick/HDD/Work/GNU/gmp-6.0.0
PATH_MPFR = /home/nick/HDD/Work/GNU/mpfr-3.1.2/src

PATH_GMP_LIB = $(PATH_GMP)/.libs
PATH_GMP_INC = $(PATH_GMP)

PATH_MPFR_LIB = $(PATH_MPFR)/.libs
PATH_MPFR_INC = $(PATH_MPFR)

OPTS = -O2 -I$(PATH_ALGLIB) -L$(PATH_ALGLIB)

LIBOPTS = -L$(PATH_GMP_LIB) -L$(PATH_MPFR_LIB) -L$(PATH_ALGLIB) -lmpalglib -lmpfr -lgmp -lm -lstdc++ -lgsl -lgslcblas 
INCOPTS = -I$(PATH_GMP_INC) -I$(PATH_MPFR_INC) -I$(PATH_ALGLIB)

LOPTS = 



# -Wall -> warning all

all: round wakeround flat wakeflat lib Makefile

roundchamber.o: roundchamber.cc
	$(CC) $(LOPTS) -fPIC -o roundchamber.o -c roundchamber.cc $(INCOPTS)

round: roundchamber.o
	$(CC) $(LOPTS) -o roundchamber.x roundchamber.o -O2 $(LIBOPTS)

wake_roundchamber.o: wake_roundchamber.cc
	$(CC) $(LOPTS) -fPIC -o wake_roundchamber.o -c wake_roundchamber.cc $(INCOPTS)

wakeround: wake_roundchamber.o
	$(CC) $(LOPTS) -o wake_roundchamber.x wake_roundchamber.o -O2 $(LIBOPTS)

flatchamber.o: flatchamber.cc
	$(CC) $(LOPTS) -fPIC -o flatchamber.o -c flatchamber.cc $(INCOPTS)

flat: flatchamber.o
	$(CC) $(LOPTS) -o flatchamber.x flatchamber.o -O2 $(LIBOPTS)

wake_flatchamber.o: wake_flatchamber.cc
	$(CC) $(LOPTS) -fPIC -o wake_flatchamber.o -c wake_flatchamber.cc $(INCOPTS)

wakeflat: wake_flatchamber.o
	$(CC) $(LOPTS) -o wake_flatchamber.x wake_flatchamber.o -O2 $(LIBOPTS)

clean:
	rm -f *.o libIW2D.so *.x

lib: wake_roundchamber.o
	$(CC) ${LOPTS} -shared -o libIW2D.so wake_roundchamber.o -O2 $(LIBOPTS) 
