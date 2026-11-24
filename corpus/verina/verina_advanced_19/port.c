#include "pfc.h"

/* Verina verina_advanced_19: 1 when s is a palindrome once non-letters are dropped and case is ignored. */
long isLetter(long c)
    ensures(result == 0 || result == 1)
{
    if ((c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z')) {
        return 1;
    }
    return 0;
}

long toLower(long c)
    ensures(result == c || (c >= 'A' && c <= 'Z' && result == c + 32))
{
    if (c >= 'A' && c <= 'Z') {
        return c - 'A' + 'a';
    }
    return c;
}

long isCleanPalindrome(long s_len, const char s[s_len])
    requires(s_len >= 0) /* a length; this spelling of the parameter does not give the checker 0 <= s_len */
    /* The postcondition compares the normalised string (a recursive filter and map) with its reverse:
     * dropped. */
    ensures(result == 0 || result == 1)
{
    long i = 0;
    long j = s_len - 1;

    while (i < j) invariant(0 <= i && j <= s_len - 1) {
        long left = s[i];
        long right = s[j];
        long left_is_letter = isLetter(left);
        long right_is_letter = isLetter(right);
        if (!left_is_letter) {
            i++;
        } else if (!right_is_letter) {
            j--;
        } else {
            long a = toLower(left);
            long b = toLower(right);
            if (a != b) {
                return 0;
            }
            i++;
            j--;
        }
    }
    return 1;
}
