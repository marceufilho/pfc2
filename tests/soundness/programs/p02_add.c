#include "pfc.h"

/* y + y can wrap. */
long probe(long n, long a[n], long x, long y)
    requires(0 <= x && x < n)
{
    long t = y + y;
    long k = x + (t / 2 - y);
    return a[k];
}
