#include "pfc.h"

/* Verina verina_basic_50: absolute value of x. */
long Abs(long x)
    ensures((x < 0 || x == result) && (x >= 0 || x + result == 0))
{
    if (x < 0) {
        return -x;
    }
    return x;
}
