#include "pfc.h"

/* Verina verina_basic_42: number of digit characters in s. */
long countDigits(long s_len, const char s[s_len])
{
    long count = 0;

    for (long i = 0; i < s_len; i++) {
        if (s[i] >= '0' && s[i] <= '9') {
            count++;
        }
    }
    return count;
}
