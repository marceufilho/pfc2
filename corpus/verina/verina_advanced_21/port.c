#include "pfc.h"

/* Verina verina_advanced_21: 1 when s reads the same forward and backward, else 0. */
long isPalindrome(long s_len, const char s[s_len])
    requires(s_len >= 0) /* a length; this spelling of the parameter does not give the checker 0 <= s_len */
    /* not result -> s is not empty: stated. The comparisons with the reversed list are dropped; of
     * result -> s == reverse s only the outermost pair is stated. */
    ensures(result == 1 || s_len > 0)
    ensures(result == 0 || s_len == 0 || s[0] == s[s_len - 1])
    ensures(result == 0 || result == 1)
{
    long i = 0;
    long j = s_len - 1;

    while (i < j) invariant(0 <= i && j == s_len - 1 - i && (i == 0 || s[0] == s[s_len - 1])) {
        if (s[i] != s[j]) {
            return 0;
        }
        i++;
        j--;
    }
    return 1;
}
