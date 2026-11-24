#include "pfc.h"

/* y * 2 can wrap; over mathematical integers k == x. */
long probe(long n, long a[n], long x, long y)
    requires(0 <= x && x < n)
{
    long t = y * 2;
    long k = x + (t / 2 - y);
    return a[k];
}
