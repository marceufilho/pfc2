#include "pfc.h"

/* Verina verina_basic_88: the list xs copied to out in order; returns the length. */
long ToArray(long xs_len, const long xs[xs_len], long out_cap, long out[out_cap])
    requires(out_cap >= xs_len)
    ensures(result == xs_len)
{
    for (long i = 0; i < xs_len; i++) {
        out[i] = xs[i];
    }
    return xs_len;
}
