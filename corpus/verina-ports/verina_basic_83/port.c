#include "pfc.h"

/* Verina verina_basic_83: a followed by b, written to out; returns the total length. */
long concat(long a_len, const long a[a_len], long b_len, const long b[b_len], long out_cap, long out[out_cap])
    requires(out_cap >= a_len + b_len)
{
    for (long i = 0; i < a_len; i++) {
        out[i] = a[i];
    }
    for (long i = 0; i < b_len; i++) {
        out[a_len + i] = b[i];
    }
    return a_len + b_len;
}
