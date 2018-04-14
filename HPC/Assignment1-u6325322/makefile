default: all

all:
	module load papi;
	module load python3/3.6.2;
	gcc -c c_module.c -fPIC -l papi -lm -pg
	gcc -shared -o c_module.so c_module.o -l papi -lm -p

