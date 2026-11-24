#include "pfc.h"

/* Verina verina_basic_8: the smaller of a and b. */
long myMin(long a, long b)
    ensures(result <= a && result <= b)
    ensures(result == a || result == b)
{
    if (a <= b) {
        return a;
    }
    return b;
}
