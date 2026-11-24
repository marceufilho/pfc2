#include "pfc.h"

/* SV-COMP c/loop-invgen/half_2.i, ported by rules H1, H2, H4, H5, H8. */
long half_2(long n)
    requires(n <= 1000000)
{
    long i = 0;
    long k = 0;
    k = n;
    i = 0;
    while (i < n) {
        k--;
        i = i + 2;
    }
    long j = 0;
    while (j < n / 2) {
        assert(k > 0);
        k--;
        j++;
    }
    return 0;
}
