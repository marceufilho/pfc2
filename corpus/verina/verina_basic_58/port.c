#include "pfc.h"

/* Verina verina_basic_58: every element of s doubled, written to out; returns the length. */
long double_array_elements(long s_len, const long s[s_len], long out_cap, long out[out_cap])
    requires(out_cap >= s_len)
    ensures(result == s_len)
{
    for (long i = 0; i < s_len; i++) {
        out[i] = 2 * s[i];
    }
    return s_len;
}
