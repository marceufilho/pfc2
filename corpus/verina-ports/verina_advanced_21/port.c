#include "pfc.h"

/* Verina verina_advanced_21: 1 when s reads the same forward and backward, else 0. */
long isPalindrome(long s_len, const char s[s_len])
{
    long i = 0;
    long j = s_len - 1;

    while (i < j) {
        if (s[i] != s[j]) {
            return 0;
        }
        i++;
        j--;
    }
    return 1;
}
