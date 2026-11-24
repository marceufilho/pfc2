#include "pfc.h"

/* Verina verina_basic_106: element-wise sum of two arrays of the same length. */
long arraySum(long a_len, const long a[a_len], long b_len, const long b[b_len], long out_cap, long out[out_cap])
    requires(a_len == b_len)
    requires(out_cap >= a_len)
    ensures(result == a_len)
{
    for (long i = 0; i < a_len; i++) invariant(0 <= i) {
        out[i] = a[i] + b[i];
    }
    return a_len;
}
