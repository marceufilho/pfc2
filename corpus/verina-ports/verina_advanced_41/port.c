#include "pfc.h"

/* Verina verina_advanced_41: the largest of three integers. */
long maxOfThree(long a, long b, long c)
{
    long best = a;

    if (b > best) {
        best = b;
    }
    if (c > best) {
        best = c;
    }
    return best;
}
