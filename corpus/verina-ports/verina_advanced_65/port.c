#include "pfc.h"

/* Verina verina_advanced_65: the characters of s in reverse order; returns the length. */
long reverseString(long s_len, const char s[s_len], long out_cap, char out[out_cap])
    requires(out_cap >= s_len)
{
    for (long i = 0; i < s_len; i++) {
        out[i] = s[s_len - 1 - i];
    }
    return s_len;
}
