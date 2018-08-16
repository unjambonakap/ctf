%module pyemu

%include "std_string.i"
%include "typemaps.i"


%{
#include "opa/emu/msp430/emu.h"

using namespace opa::emu::msp430;
%}

%typemap(in) u16 {
    $1=PyLong_AsUnsignedLong($input);
}
%typemap(in) const std::string& (std::string temp, char *buf){
    buf=PyBytes_AsString($input);
    printf(">> GOT >> %p\n", buf);
    buf=strdup(buf);
    temp=buf;
    $1=&temp;
}

%typemap(freearg) const std::string& {
free(buf$argnum);
}
%include "opa/emu/msp430/emu.h"
