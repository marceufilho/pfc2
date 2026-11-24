#include "pfc.h"

/* Verina verina_basic_61: 1 when every character of s is a digit (also for an empty string), else 0. */
long allDigits(long s_len, const char s[s_len])
    ensures(result == 0 || result == 1)
{
    for (long i = 0; i < s_len; i++) {
        if (s[i] < '0' || s[i] > '9') {
            return 0;
        }
    }
    return 1;
}
