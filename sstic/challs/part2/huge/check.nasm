
bits 64
global _start





;0x99a380575a7: movdqa xmm0, xmmword ptr [rsp] 
;ReadEvent addr:000000000010ec00 n:0000000000000008 val:24b87838d17e8929 :addr:000000000010ec08 n:0000000000000008 val:ec1b34898cc04ed5 
;0x99a380575ac: movdqa xmm1, xmmword ptr [rip + 0x6c] 
;ReadEvent addr:0000099a38057620 n:0000000000000008 val:2be6a9b2c5cbfdcc :addr:0000099a38057628 n:0000000000000008 val:194f2e0e37877e0d 

section .text
_start:
mov rax, 0ec1b34898cc04ed5h
mov rbx, 024b87838d17e8929h
PINSRQ xmm0, rax, 0
PINSRQ xmm0, rbx, 1
mov rax, 0194f2e0e37877e0dh
mov rbx, 02be6a9b2c5cbfdcch
PINSRQ xmm1, rax, 0
PINSRQ xmm1, rbx, 1
pxor xmm0, xmm1
movdqa xmm1, xmm0
psrlw xmm1, 4


xor edx, edx 
xor ecx, ecx 
mov dl, 0xf 
mov cl, dl 
xchg cl, dh 
mov cx, dx 
bswap ecx 
or edx, ecx 
movd xmm2, edx 
pshufd xmm2, xmm2, 0 
pand xmm0, xmm2 
pand xmm1, xmm2 
movdqa xmm2, xmm1 
punpcklbw xmm1, xmm0 
punpckhbw xmm2, xmm0 

;0x2c7affef62e4: movdqa xmmword ptr [rdi], xmm1 		 <<<< TRACEVENT, rax=0010ec00
;WriteEvent addr:000000000010ec00 n:0000000000000008 nval:0401050b0407050e val:24b87838d17e8929 :addr:000000000010ec08 n:0000000000000008 nval:0f000e05010d0a08 val:ec1b34898cc04ed5 
;0x2c7affef62e8: movdqa xmmword ptr [rdi + 0x10], xmm2 		 <<<< TRACEVENT, rax=0010ec00
;WriteEvent addr:000000000010ec10 n:0000000000000008 nval:0b0b07040003080d val:000000001e716dcb :addr:000000000010ec18 n:0000000000000008 nval:050f04050a010708 val:4345423134333ffe 
