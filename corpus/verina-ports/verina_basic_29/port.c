#include "pfc.h"

/* Verina verina_basic_29: s without its element at index k. */
long removeElement(long s_len, const long s[s_len], long k, long out_cap, long out[out_cap])
    requires(0 <= k && k < s_len)
    requires(out_cap >= s_len - 1)
{
    for (long i = 0; i < k; i++) {
        out[i] = s[i];
    }
    for (long i = k + 1; i < s_len; i++) {
        out[i - 1] = s[i];
    }
    return s_len - 1;
}
