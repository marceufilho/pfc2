#include "pfc.h"

/* Verina verina_basic_14: 1 when the string contains 'z' or 'Z', else 0. */
long containsZ(long s_len, const char s[s_len])
{
    for (long i = 0; i < s_len; i++) {
        if (s[i] == 'z' || s[i] == 'Z') {
            return 1;
        }
    }
    return 0;
}
