#include "pfc.h"

/* Verina verina_basic_92: out[0] = Y, out[1] = X. */
long SwapArithmetic(long X, long Y, long out_cap, long out[out_cap])
    requires(out_cap >= 2)
{
    out[0] = Y;
    out[1] = X;
    return 0;
}
