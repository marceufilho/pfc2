#include "pfc.h"

/* Verina verina_basic_81: out[0] = remainder, out[1] = quotient of x by y; (x, 0) when y is 0. */
long DivisionFunction(long x, long y, long out_cap, long out[out_cap])
    requires(x >= 0)
    requires(y >= 0)
    requires(out_cap >= 2)
    ensures(y != 0 || (out[0] == x && out[1] == 0))
    ensures(y == 0 || (out[1] * y + out[0] == x && 0 <= out[0] && out[0] < y && 0 <= out[1]))
{
    if (y == 0) {
        out[0] = x;
        out[1] = 0;
        return 0;
    }
    out[0] = x % y;
    out[1] = x / y;
    return 0;
}
