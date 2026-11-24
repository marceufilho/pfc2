#include "pfc.h"

/* Verina verina_advanced_19: 1 when s is a palindrome once non-letters are dropped and case is ignored. */
long isLetter(long c)
{
    if ((c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z')) {
        return 1;
    }
    return 0;
}

long toLower(long c)
{
    if (c >= 'A' && c <= 'Z') {
        return c - 'A' + 'a';
    }
    return c;
}

long isCleanPalindrome(long s_len, const char s[s_len])
{
    long i = 0;
    long j = s_len - 1;

    while (i < j) {
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
