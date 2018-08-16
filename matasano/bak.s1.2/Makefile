all: c

LIB=-lssl -lcrypto
flag= -g

c: helper.o c.cpp
	g++  $(flag) $(LIB) -g helper.o d.cpp
helper.o: helper.cpp helper.h
	g++  $(flag) $(LIB) -g -c helper.cpp
