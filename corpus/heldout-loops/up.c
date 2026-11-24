#include "pfc.h"

/* SV-COMP c/loop-invgen/up.i, ported by rules H1, H4, H5, H8. */
long up(long n)
{
    long i = 0;
    long k = 0;
    while (i < n) {
        i++;
        k++;
    }
    long j = 0;
    while (j < n) {
        assert(k > 0);
        j++;
        k--;
    }
    return 0;
}
