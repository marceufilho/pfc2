#include "pfc.h"

/* The middle of a range, written so that no intermediate value can leave the range of a long. */
long mid(long lo, long hi)
    requires(0 <= lo && lo <= hi)
    ensures(lo <= result && result <= hi)
{
    return lo + (hi - lo) / 2;
}
