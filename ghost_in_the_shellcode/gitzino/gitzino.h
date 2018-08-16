#ifndef _H_GITZINO
#define _H_GITZINO

#include <opa_common.h>

static const char *db_file = "perm_db.out";
static const int n = 52;

u32 get_perm_key(u32 *tmp) {
    u32 res = 0;
    REP(i, 5) res = n * res + tmp[i];
    return res;
}

#endif
