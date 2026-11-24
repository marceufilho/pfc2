#include "pfc.h"

/* Verina verina_basic_55: 1 when a equals b, else 0. */
long Compare(long a, long b)
    ensures((a != b || result == 1) && (a == b || result == 0))
{
    if (a == b) {
        return 1;
    }
    return 0;
}
