#include "pfc.h"

/* The wrapping value travels through a global. */
long g = 0;

long probe(long n, long a[n], long x, long y)
    requires(0 <= x && x < n)
{
    g = y * 2;
    long k = x + (g / 2 - y);
    return a[k];
}
