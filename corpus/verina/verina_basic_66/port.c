#include "pfc.h"

/* Verina verina_basic_66: 1 when x is even, else 0. */
long ComputeIsEven(long x)
    ensures(result == 0 || result == 1)
{
    if (x % 2 == 0) {
        return 1;
    }
    return 0;
}
