#include "pfc.h"

/* Verina verina_basic_65: integer square root of N: the largest r with r * r <= N. */
long SquareRoot(long N)
    requires(N >= 0)
    ensures(0 <= result && result * result <= N && N < (result + 1) * (result + 1))
{
    long r = 0;

    while ((r + 1) * (r + 1) <= N) invariant(0 <= r && r * r <= N) {
        r++;
    }
    return r;
}
