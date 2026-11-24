#include "pfc.h"

/* Verina verina_basic_72: a followed by b, written to out; returns the new length. */
long append(long a_len, const long a[a_len], long b, long out_cap, long out[out_cap])
    requires(out_cap >= a_len + 1)
{
    for (long i = 0; i < a_len; i++) {
        out[i] = a[i];
    }
    out[a_len] = b;
    return a_len + 1;
}
