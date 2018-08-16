

res: solve.cpp test.asm
	nasm ./test.asm -f elf64 -l test.lst
	g++ -g -std=c++11 solve.cpp test.o -o solve


