#include "pfc.h"

/* Verina verina_basic_33: smallest natural number missing from a sorted list of naturals. */
long smallestMissingNumber(long s_len, const long s[s_len])
{
    long missing = 0;

    for (long i = 0; i < s_len; i++) {
        if (s[i] == missing) {
            missing++;
        } else if (s[i] > missing) {
            break;
        }
    }
    return missing;
}
