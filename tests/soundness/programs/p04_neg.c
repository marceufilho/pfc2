#include "pfc.h"

/* -y wraps for the smallest long. */
long probe(long n, long a[n], long x, long y)
    requires(0 <= x && x < n)
{
    long t = -y;
    long k = x + (t + y);
    return a[k];
}
