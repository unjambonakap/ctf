global doRound_entry
DEFAULT ABS
doRound_entry:
;fd
;ret=int

    mov eax, [esp+4]
    sub esp, 4
    mov [esp], eax
    mov eax, 0x80496ae
    call eax
    add esp, 4
    retn


