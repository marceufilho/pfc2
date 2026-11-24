#include "pfc.h"

/* Two products that cancel over mathematical integers. */
long probe(long n, long a[n], long x, long y)
    requires(0 <= x && x < n)
{
    long t = y * y;
    long u = t - y * y;
    long k = x + u;
    return a[k];
}
