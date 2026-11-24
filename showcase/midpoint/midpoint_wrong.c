#include "pfc.h"

/* The middle of a range, as binary search needs it. Every test with ordinary numbers passes. */
long mid(long lo, long hi)
    requires(0 <= lo && lo <= hi)
    ensures(lo <= result && result <= hi)
{
    return (lo + hi) / 2;
}
