#include "pfc.h"

/* SV-COMP c/loop-invgen/seq-3.i, ported by rules H1, H2, H4, H5, H8. */
long seq_3(long n0, long n1)
    requires(-1000000 <= n0 && n0 < 1000000)
    requires(-1000000 <= n1 && n1 < 1000000)
{
    long i0 = 0;
    long k = 0;
    while (i0 < n0) {
        i0++;
        k++;
    }
    long i1 = 0;
    while (i1 < n1) {
        i1++;
        k++;
    }
    long j1 = 0;
    while (j1 < n0 + n1) {
        assert(k > 0);
        j1++;
        k--;
    }
    return 0;
}
