#include "pfc.h"

/* Verina verina_basic_1: 1 when a and b have opposite signs (zero has no sign), else 0. */
long hasOppositeSign(long a, long b)
    ensures(!((a < 0 && b > 0) || (a > 0 && b < 0)) || result == 1)
    ensures(((a < 0 && b > 0) || (a > 0 && b < 0)) || result == 0)
{
    if ((a < 0 && b > 0) || (a > 0 && b < 0)) {
        return 1;
    }
    return 0;
}
