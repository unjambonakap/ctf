
PYTHON_FLAGS = -I/home/benoit/opt32/include/python2.7 -L/home/benoit/opt32/lib/ -lpython2.7
LIBS = $(PYTHON_FLAGS) -ldl -lpthread
OBJS = trampoline.o random.o random_r.o

all: appServer.so


trampoline.o: trampoline.S
	nasm -f elf trampoline.S
random.o: random.c 
	gcc -m32 -fPIC -c random.c random_r.c
random_r.o: random_r.c 
	gcc -m32 -fPIC -c random_r.c

appServer.so: appServer.cpp $(OBJS)
	g++ -m32 -shared -fPIC appServer.cpp $(OBJS) -o appServer.so $(LIBS)

test: appServer test.cpp
	g++ -m32 test.cpp -ldl

