#include "pfc.h"

/* Verina verina_basic_42: number of digit characters in s. */
long countDigits(long s_len, const char s[s_len])
    requires(s_len >= 0) /* a length; this spelling of the parameter does not give the checker 0 <= s_len */
    ensures(0 <= result)
{
    long count = 0;

    for (long i = 0; i < s_len; i++) invariant(0 <= i && i <= s_len && 0 <= count && count <= i) decreases(s_len - i) {
        if (s[i] >= '0' && s[i] <= '9') {
            count++;
        }
    }
    return count;
}
