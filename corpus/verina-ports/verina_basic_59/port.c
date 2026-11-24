#include "pfc.h"

/* Verina verina_basic_59: out[0] = 2 * x and out[1] = 4 * x. */
long DoubleQuadruple(long x, long out_cap, long out[out_cap])
    requires(out_cap >= 2)
{
    out[0] = 2 * x;
    out[1] = 4 * x;
    return 0;
}
