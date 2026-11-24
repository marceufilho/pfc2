#include "pfc.h"

/* Verina verina_basic_16: a copy of s with every oldChar replaced by newChar. */
long replaceChars(long s_len, const char s[s_len], long oldChar, long newChar, long out_cap, char out[out_cap])
    requires(out_cap >= s_len)
    ensures(result == s_len)
{
    for (long i = 0; i < s_len; i++) invariant(0 <= i) {
        if (s[i] == oldChar) {
            out[i] = newChar;
        } else {
            out[i] = s[i];
        }
    }
    return s_len;
}
