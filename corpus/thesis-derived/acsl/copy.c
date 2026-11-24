/* Adapted from ACSL by Example; see ../PROVENANCE.json and ../LICENSE. */
#include "pfc.h"

long copy(const long a[], long a_len, long b[], long b_len, long n) {
    REQUIRES(0 <= n && n <= a_len && n <= b_len);
    REQUIRES(SEPARATED(a, a_len, b, b_len));
    for (long i = 0; i < n; i = i + 1) {
        INVARIANT(0 <= i && i <= n);
        b[i] = a[i];
    }
    return n;
}

