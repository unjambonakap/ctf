all: c

LIB=-lssl -lcrypto -lgmp
flag= -g -O9

c: crypto.o helper.o e.cpp
	g++  $(flag) $(LIB) helper.o crypto.o e.cpp
helper.o: helper.cpp helper.h
	g++  $(flag) $(LIB) -c helper.cpp
crypto.o: crypto.cpp crypto.h
	g++  $(flag) $(LIB) -c crypto.cpp
