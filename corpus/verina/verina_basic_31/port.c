#include "pfc.h"

/* Verina verina_basic_31: a copy of s with every lowercase letter made uppercase (toupper written out). */
long toUppercase(long s_len, const char s[s_len], long out_cap, char out[out_cap])
    requires(s_len >= 0) /* a length; this spelling of the parameter does not give the checker 0 <= s_len */
    requires(out_cap >= s_len)
    ensures(result == s_len)
{
    for (long i = 0; i < s_len; i++) invariant(0 <= i && i <= s_len) decreases(s_len - i) {
        if (s[i] >= 'a' && s[i] <= 'z') {
            out[i] = s[i] - 'a' + 'A';
        } else {
            out[i] = s[i];
        }
    }
    return s_len;
}
