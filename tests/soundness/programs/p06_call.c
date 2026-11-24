#include "pfc.h"

/* The wrap happens inside a callee; the caller relies on the callee's postcondition. */
long twice(long v)
    ensures(result == v * 2)
{
    return v * 2;
}

long probe(long n, long a[n], long x, long y)
    requires(0 <= x && x < n)
{
    long k = x + (twice(y) / 2 - y);
    return a[k];
}
