#include "pfc.h"

/* Verina verina_advanced_59: 1 when s is a palindrome ignoring case and non-alphanumeric characters. */
long is_alnum(long c)
{
    if ((c >= '0' && c <= '9') || (c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z')) {
        return 1;
    }
    return 0;
}

long to_lower(long c)
{
    if (c >= 'A' && c <= 'Z') {
        return c - 'A' + 'a';
    }
    return c;
}

long palindromeIgnoreNonAlnum(long s_len, const char s[s_len])
    requires(0 <= s_len)
    ensures(result == 0 || result == 1)
{
    long i = 0;
    long j = s_len - 1;

    while (i < j) invariant(0 <= i && j <= s_len - 1) {
        long left = s[i];
        long right = s[j];

        if (!is_alnum(left)) {
            i++;
            continue;
        }
        if (!is_alnum(right)) {
            j--;
            continue;
        }
        if (to_lower(left) != to_lower(right)) {
            return 0;
        }
        i++;
        j--;
    }
    return 1;
}
