#include "pfc.h"

/* Verina verina_basic_65: integer square root of N: the largest r with r * r <= N. */
long SquareRoot(long N)
{
    long r = 0;

    while ((r + 1) * (r + 1) <= N) {
        r++;
    }
    return r;
}
