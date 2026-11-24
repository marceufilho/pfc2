#include "pfc.h"

/* Verina verina_basic_17: a copy of s with every uppercase letter made lowercase (tolower written out). */
long toLowercase(long s_len, const char s[s_len], long out_cap, char out[out_cap])
    requires(out_cap >= s_len)
{
    for (long i = 0; i < s_len; i++) {
        if (s[i] >= 'A' && s[i] <= 'Z') {
            out[i] = s[i] - 'A' + 'a';
        } else {
            out[i] = s[i];
        }
    }
    return s_len;
}
