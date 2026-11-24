#include "pfc.h"

/* The wrapping product is computed before the loop; every access in the loop depends on it. */
long probe(long n, long a[n], long x, long y)
    requires(0 <= x && x < n)
{
    long t = y * 2;
    long s = 0;

    for (long i = 0; i < n; i++) {
        s = a[i + (t / 2 - y)];
    }
    return s;
}
