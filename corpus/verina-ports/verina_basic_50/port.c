#include "pfc.h"

/* Verina verina_basic_50: absolute value of x. */
long Abs(long x)
{
    if (x < 0) {
        return -x;
    }
    return x;
}
