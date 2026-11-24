#include "pfc.h"

/* Verina verina_basic_30: element-wise modulo of a by b, never negative (no element of b is zero). */
long elementWiseModulo(long a_len, const long a[a_len], long b_len, const long b[b_len], long out_cap, long out[out_cap])
    requires(a_len == b_len)
    requires(out_cap >= a_len)
{
    for (long i = 0; i < a_len; i++) {
        long rest = a[i] % b[i];

        if (rest < 0) {
            if (b[i] < 0) {
                rest -= b[i];
            } else {
                rest += b[i];
            }
        }
        out[i] = rest;
    }
    return a_len;
}
