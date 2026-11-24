#include "pfc.h"

/* Verina verina_basic_85: a in reverse order, written to out; returns the length. */
long reverse(long a_len, const long a[a_len], long out_cap, long out[out_cap])
    requires(out_cap >= a_len)
    ensures(result == a_len)
{
    for (long i = 0; i < a_len; i++) {
        out[i] = a[a_len - 1 - i];
    }
    return a_len;
}
