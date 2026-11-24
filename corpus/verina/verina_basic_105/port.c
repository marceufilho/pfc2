#include "pfc.h"

/* Verina verina_basic_105: element-wise product of a and b; an element missing from b counts as 0. */
long arrayProduct(long a_len, const long a[a_len], long b_len, const long b[b_len], long out_cap, long out[out_cap])
    requires(out_cap >= a_len)
    requires(a_len == b_len)
    ensures(result == a_len)
{
    for (long i = 0; i < a_len; i++) invariant(0 <= i) {
        long other = 0;

        if (i < b_len) {
            other = b[i];
        }
        out[i] = a[i] * other;
    }
    return a_len;
}
