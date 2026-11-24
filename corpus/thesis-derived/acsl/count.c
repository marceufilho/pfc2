/* Adapted from ACSL by Example; see ../PROVENANCE.json and ../LICENSE. */
#include "pfc.h"

long count(const long a[], long a_len, long n, long v) {
    REQUIRES(0 <= n && n <= a_len);
    long counted = 0;
    for (long i = 0; i < n; i = i + 1) {
        INVARIANT(0 <= counted && counted <= i && i <= n);
        if (a[i] == v) { counted = counted + 1; }
    }
    return counted;
}

