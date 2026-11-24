#include "pfc.h"

/* Verina verina_basic_36: s with every space, comma and dot replaced by a colon; returns the length. */
long replaceWithColon(long s_len, const char s[s_len], long out_cap, char out[out_cap])
    requires(out_cap >= s_len)
{
    for (long i = 0; i < s_len; i++) {
        if (s[i] == ' ' || s[i] == ',' || s[i] == '.') {
            out[i] = ':';
        } else {
            out[i] = s[i];
        }
    }
    return s_len;
}
