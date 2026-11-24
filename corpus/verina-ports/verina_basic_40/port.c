#include "pfc.h"

/* Verina verina_basic_40: the second-smallest value of s (the smallest value larger than the minimum). */
long secondSmallest(long s_len, const long s[s_len])
    requires(s_len >= 2)
{
    long smallest = s[0];
    long second = s[0];
    _Bool found = 0;

    for (long i = 1; i < s_len; i++) {
        if (s[i] < smallest) {
            smallest = s[i];
        }
    }
    for (long i = 0; i < s_len; i++) {
        if (s[i] > smallest && (!found || s[i] < second)) {
            second = s[i];
            found = 1;
        }
    }
    return second;
}
