#include "pfc.h"

/* Verina verina_basic_78: out[0] = x + y, out[1] = x - y. */
long MultipleReturns(long x, long y, long out_cap, long out[out_cap])
    requires(out_cap >= 2)
    ensures(out[0] == x + y && out[1] + y == x)
{
    out[0] = x + y;
    out[1] = x - y;
    return 0;
}
