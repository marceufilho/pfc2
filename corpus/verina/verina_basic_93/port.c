#include "pfc.h"

/* Verina verina_basic_93: out[0] = Y, out[1] = X (8-bit unsigned values held in long). */
long SwapBitvectors(long X, long Y, long out_cap, long out[out_cap])
    requires(out_cap >= 2)
    ensures(out[0] == Y && out[1] == X)
    ensures(X == Y || (out[0] != X && out[1] != Y))
{
    out[0] = Y;
    out[1] = X;
    return 0;
}
