#include "pfc.h"

/* SV-COMP c/loop-invgen/down.i, ported by rules H1, H4, H5, H8. */
long down(long n)
{
    long k = 0;
    long i = 0;
    while (i < n) {
        i++;
        k++;
    }
    long j = n;
    while (j > 0) {
        assert(k > 0);
        j--;
        k--;
    }
    return 0;
}
