#include "pfc.h"

/* Verina verina_basic_73: 1 when s matches pattern p of the same length, where '?' in p matches any character. */
long Match(long s_len, const char s[s_len], long p_len, const char p[p_len])
{
    if (s_len != p_len) {
        return 0;
    }
    for (long i = 0; i < s_len; i++) {
        if (s[i] != p[i] && p[i] != '?') {
            return 0;
        }
    }
    return 1;
}
