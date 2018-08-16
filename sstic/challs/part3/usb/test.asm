BITS 64
extern memcpy
extern exit

global main2
global init_rc5
global decrypt_rc5


%define var_1D8   -1D8h
%define var_1D4   -1D4h
%define var_108   -108h
%define var_8   -8
%define arg_0   8
%define arg_8   10h

section .data
a551c2016b00b5f db "551C2016B00B5F00"
alignb 16
s_buf: times 1000 db 0
alignb 16
res_buf: times 1000 db 0
alignb 16

;test_buf: db `\x83\x56\x26\x91\xfc\x37\xd2\x85\x07\xa4\xbc\xef\x45\x46\x60\xd7`
test_buf: db `|\xc9\x0e\xd9]\xc8\x13T\x93\xbc\xc4W\xab8\x03\xb2L\x84\x06\xa7u\xe6\xdb\x8c\x93\x8c\xadq)"{\x08`
alignb 16


section .text

main2:
mov rcx, s_buf
call init_rc5
mov rcx, s_buf
mov rdx, test_buf
mov r8, res_buf
call decrypt_rc5
call end

end:
mov edi, 0
call exit

init_rc5:
sub rsp, 100h
mov     [rsp+arg_0], rbx
mov     [rsp+arg_8], rsi
push rsi
push rdx
push rdi
push rcx
push rbx
push r8
push r9
push r10
mov rcx, rdi
sub rsp, 1F0h
mov rbx, rcx
xor r8d, r8d
xor ecx, ecx
xor edx, edx
mov r10, a551c2016b00b5f ; "551C2016B00B5F00"
lea r9, [rsp+1F8h+var_108]
..@loc_11E3F:       ; CODE XREF: looks_liek_rc5_init+4Dj
movzx eax, byte [r10]
shl edx, 8
inc ecx
or  edx, eax
inc r10
test  cl, 3
jnz short ..@loc_11E5E
mov [r9], edx
inc r8d
add r9, 4
xor edx, edx

..@loc_11E5E:       ; CODE XREF: looks_liek_rc5_init+3Cj
cmp ecx, 10h
jb  short ..@loc_11E3F
mov dword [rsp+1F8h+var_1D8], 0B7E15163h
lea rcx, [rsp+1F8h+var_1D4]
mov edx, 2Bh

..@loc_11E75:       ; CODE XREF: looks_liek_rc5_init+73j
mov eax, [rcx-4]
sub eax, 61C88647h
mov [rcx], eax
add rcx, 4
sub rdx, 1
jnz short ..@loc_11E75
lea ecx, [rdx+2Ch]
mov eax, r8d
cmp r8d, ecx
cmovb eax, ecx
xor esi, esi
xor r11d, r11d
lea ecx, [rax+rax*2]
xor r9d, r9d
xor edi, edi
test  ecx, ecx
jz  short ..@loc_11EFB
mov r10d, ecx

..@loc_11EA9:       ; CODE XREF: looks_liek_rc5_init+E5j
mov eax, [rsp+r11*4+1F8h+var_1D8]
add eax, r9d
add edi, eax
mov eax, esi
ror edi, 3
mov [rsp+r11*4+1F8h+var_1D8], edi
lea ecx, [r9+rdi]
add r9d, edi
add r9d, [rsp+rax*4+1F8h+var_108]
inc r11d
ror r9d, cl
mov [rsp+rax*4+1F8h+var_108], r9d
mov eax, 0BA2E8BA3h
mul r11d
shr edx, 5
lea eax, [rsi+1]
imul  edx, 2Ch
sub r11d, edx
xor edx, edx
div r8d
sub r10, 1
mov esi, edx
jnz short ..@loc_11EA9

..@loc_11EFB:       ; CODE XREF: looks_liek_rc5_init+90j
lea rsi, [rsp+1F8h+var_1D8]
mov rdx, 0B0h
mov rdi, rbx
call memcpy
and dword [rbx+0B0h], 0
and dword [rbx+0B4h], 0
and dword [rbx+0B8h], 0
and dword [rbx+0BCh], 0
lea r11, [rsp+1F8h+var_8]
mov rbx, [r11+10h]
mov rsi, [r11+18h]
mov rsp, r11
push r10
push r9
push r8
pop rbx
pop rcx
pop rdi
pop rdx
pop rsi
add rsp, 100h
retn

decrypt_rc5:
; DATA XREF: .pdata:00000000002160CCo

%define arg_0   8
%define arg_8   10h
%define arg_10    18h
%define arg_18    20h

sub rsp, 100h
mov rax, rsp
mov [rax+8], rbx
mov [rax+10h], rbp
mov [rax+18h], rsi
mov [rax+20h], rdi
push rbp
push rbx
push rcx
push rdx
push  r8
push  r9
push  r12
push  r13
push  r14
push  r15
mov rcx, rdi
mov rdx, rsi
mov r8, rsi
mov r10d, [rdx]
mov r11d, [rdx+8]
mov ebx, [rdx+0Ch]
mov rdi, r8
mov r8d, [rdx+4]
mov esi, r10d
sub r10d, [rcx+0A8h]
mov r12d, r11d
sub r11d, [rcx+0ACh]
mov r9, rcx
mov ebp, r8d
mov r13d, ebx
mov r15d, 13h
lea r14, [rcx+0A0h]

loc_1208E:        ; CODE XREF: decrypt_rc5+99j
mov eax, ebx
mov ebx, r11d
mov r11d, r8d
sub r11d, [r14+4]
mov r8d, r10d
mov r10d, eax
sub r10d, [r14]
lea edx, [r8+r8+1]
lea eax, [rbx+rbx+1]
imul  edx, r8d
ror edx, 5
imul  eax, ebx
ror eax, 5
mov ecx, edx
sub r14, 8
rol r11d, cl
mov ecx, eax
xor r11d, eax
rol r10d, cl
xor r10d, edx
sub r15, 1
jns short loc_1208E
xor r10d, [r9+0B0h]
xor r11d, [r9+0B8h]
sub r8d, [r9]
xor r8d, [r9+0B4h]
sub ebx, [r9+4]
mov [r9+0B0h], esi
xor ebx, [r9+0BCh]
mov rsi, [rsp+20h+arg_10]
mov [r9+0B4h], ebp
mov rbp, [rsp+20h+arg_8]
mov [rdi+0Ch], ebx
mov rbx, [rsp+20h+arg_0]
mov [rdi], r10d
mov [rdi+4], r8d
mov [rdi+8], r11d
mov rdi, [rsp+20h+arg_18]
mov [r9+0B8h], r12d
mov [r9+0BCh], r13d
pop r15
pop r14
pop r13
pop r12
pop r9
pop r8
pop rdx
pop rcx
pop rbx
pop rbp
add rsp, 100h
retn
