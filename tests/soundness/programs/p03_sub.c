#include "pfc.h"

/* 0 - y and t - y can wrap; u is -2y. */
long probe(long n, long a[n], long x, long y)
    requires(0 <= x && x < n)
{
    long t = 0 - y;
    long u = t - y;
    long k = x - (u / 2 + y);
    return a[k];
}
