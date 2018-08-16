all: c

LIB=-lssl -lcrypto
c: lib.o c.cpp
	g++ -w $(LIB) -fpermissive -g lib.o c.cpp
lib.o: lib.cpp lib.h
	g++ -w $(LIB) -fpermissive -g -c lib.cpp
