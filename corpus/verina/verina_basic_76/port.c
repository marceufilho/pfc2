#include "pfc.h"

/* Verina verina_basic_76: the smaller of x and y. */
long myMin(long x, long y)
    ensures(x > y || result == x)
    ensures(x <= y || result == y)
{
    if (x <= y) {
        return x;
    }
    return y;
}
