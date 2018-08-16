
all: solve verifier.exe

solve: solve.cpp
	g++ -O9 solve.cpp -o solve -std=c++11  -pthread
verifier.exe: verifier.cs
	dmcs verifier.cs -out:verifier.exe


