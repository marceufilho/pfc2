#include "pfc.h"

/* A write: without the trap the wrapped index would corrupt memory far from the array. */
long probe(long n, long a[n], long x, long y)
    requires(0 <= x && x < n)
{
    long t = y * 2;
    long k = x + (t / 2 - y);

    a[k] = 7;
    return a[k];
}
