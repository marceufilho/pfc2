#include "pfc.h"

/* Verina verina_basic_6: minimum of a, b and c. */
long minOfThree(long a, long b, long c)
{
    long min = a;

    if (b < min) {
        min = b;
    }
    if (c < min) {
        min = c;
    }
    return min;
}
