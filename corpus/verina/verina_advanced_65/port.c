#include "pfc.h"

/* Verina verina_advanced_65: the characters of s in reverse order; returns the length. */
long reverseString(long s_len, const char s[s_len], long out_cap, char out[out_cap])
    requires(out_cap >= s_len)
    requires(0 <= s_len)
    requires(separated(out, s))
    ensures(result == s_len)
    /* The two ends of the dropped element-wise equality with the reversed input. */
    ensures(s_len == 0 || (out[0] == s[s_len - 1] && out[s_len - 1] == s[0]))
{
    for (long i = 0; i < s_len; i++) invariant(0 <= i && i <= s_len && (i == 0 || out[0] == s[s_len - 1]) && (i < s_len || s_len == 0 || out[s_len - 1] == s[0])) decreases(s_len - i) {
        out[i] = s[s_len - 1 - i];
    }
    return s_len;
}
