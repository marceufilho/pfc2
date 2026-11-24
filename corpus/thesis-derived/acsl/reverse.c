/* Adapted from ACSL by Example; see ../PROVENANCE.json and ../LICENSE. */
#include "pfc.h"

long reverse(long a[], long a_len, long n) {
    REQUIRES(0 <= n && n <= a_len);
    long half = n / 2;
    for (long i = 0; i < half; i = i + 1) {
        INVARIANT(0 <= i && i <= half && half <= n - i);
        long saved = a[i];
        a[i] = a[n - 1 - i];
        a[n - 1 - i] = saved;
    }
    return n;
}

