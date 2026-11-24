/* Adapted from ACSL by Example; see ../PROVENANCE.json and ../LICENSE. */
#include "pfc.h"

long accumulate(const long a[], long a_len, long n, long init) {
    REQUIRES(0 <= n && n <= a_len);
    for (long i = 0; i < n; i = i + 1) {
        INVARIANT(0 <= i && i <= n);
        init = init + a[i];
    }
    return init;
}

