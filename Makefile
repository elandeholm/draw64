CC=gcc
CFLAGS=-fPIC -g -march=native
#LDFLAGS=-lSDL -lc
#INCL=-I/usr/include/SDL2
MODULE=libpixels
RM=rm -f
MV=mv

$(MODULE).so: pixels.o
	$(CC) -shared -Wl,-soname,$(MODULE).so pixels.o -lSDL2 -o $(MODULE).so 

pixels.o: pixels.c
	$(CC) $(CFLAGS) -c pixels.c -o pixels.o

clean:
	$(RM) pixels.o $(MODULE).so

cleanallthethings:
	$(RM) pixels.o $(MODULE).so

