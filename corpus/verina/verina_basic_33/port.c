#include "pfc.h"

/* Verina verina_basic_33: smallest natural number missing from a sorted list of naturals. */
long smallestMissingNumber(long s_len, const long s[s_len])
    requires(s_len >= 0) /* a length; this spelling of the parameter does not give the checker 0 <= s_len */
    ensures(0 <= result)
{
    long missing = 0;

    for (long i = 0; i < s_len; i++) invariant(0 <= i && i <= s_len && 0 <= missing && missing <= i) {
        if (s[i] == missing) {
            missing++;
        } else if (s[i] > missing) {
            break;
        }
    }
    return missing;
}
