/* Adapted from ACSL by Example; see ../PROVENANCE.json and ../LICENSE. */
#include "pfc.h"

long replace(long a[], long a_len, long n, long v, long w) {
    REQUIRES(0 <= n && n <= a_len);
    for (long i = 0; i < n; i = i + 1) {
        INVARIANT(0 <= i && i <= n);
        if (a[i] == v) { a[i] = w; }
    }
    return n;
}

