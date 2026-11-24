#include "pfc.h"

/* Verina verina_basic_38: 1 when all characters of s are the same (also for an empty string), else 0. */
long allCharactersSame(long s_len, const char s[s_len])
{
    for (long i = 1; i < s_len; i++) {
        if (s[i] != s[0]) {
            return 0;
        }
    }
    return 1;
}
