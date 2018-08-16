


loc_804C9B0:				; CODE XREF: sub_8048660+443Bj
		fld	qword ptr [ebp+0]
		mov	edi, ebp
		mov	byte ptr [esp+ecx+1D0h], 0
		fstp	tbyte ptr [esi]
		mov	ebp, [ebx-90h]
		fld	qword ptr [ebx+ebp*8-38h]
		mov	ebp, ebx
		mov	byte ptr [esp+edx+1D0h], 0
		fstp	tbyte ptr [eax]
		fld	ds:tbyte_8053900
		mov	ebx, [esp+140h]
		mov	byte ptr [esp+ebx+1D0h], 0
		mov	ebx, [esp+50h]
		fld	st
		fstp	tbyte ptr [ebx]
		cmp	byte ptr [esp+edx+1D0h], 3
		fld	st(1)
		jz	short loc_804CA02
		fstp	st
		fld	tbyte ptr [eax]
