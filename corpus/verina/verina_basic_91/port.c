#include "pfc.h"

/* Verina verina_basic_91: out[0] = Y, out[1] = X. */
long Swap(long X, long Y, long out_cap, long out[out_cap])
    requires(out_cap >= 2)
    ensures(out[0] == Y && out[1] == X)
    ensures(X == Y || (out[0] != X && out[1] != Y))
{
    out[0] = Y;
    out[1] = X;
    return 0;
}
