#include "opa_inc.h"

ENTRY(entry_initRand)
    push 4(%esp)
    mov $0x0804A4F0, %eax
    call *%eax
    pop %eax
    ret
END(entry_initRand)


ENTRY(entry_genRand)
    mov $0x0804A630, %eax
    call *%eax
    ret

END(entry_genRand)

ENTRY(entry_test1)
    push %ebp
    push %edi
    push %esi
    push %ebx
    push %ecx
    push %edx
    mov 0x1c(%esp), %ebx


    mov $0x8048e3f, %eax
    call *%eax
    mov %edx, %eax

    pop %edx
    pop %ecx
    pop %ebx
    pop %esi
    pop %edi
    pop %ebp
    ret
END(entry_test1)
