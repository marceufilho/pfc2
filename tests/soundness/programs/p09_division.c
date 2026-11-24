#include "pfc.h"

/* A division whose divisor is 1 over mathematical integers. */
long probe(long n, long a[n], long x, long y)
    requires(0 <= x && x < n)
{
    long t = y * 2;
    long d = 1 + (t / 2 - y);
    return a[x] / d;
}
