#include "pfc.h"

/* Verina verina_advanced_66: the words of the string in reverse order, separated by single spaces; returns the
 * length of the result. */
long reverseWords(long words_str_len, const char words_str[words_str_len], long out_cap, char out[out_cap])
    requires(out_cap >= words_str_len)
    requires(0 <= words_str_len)
    requires(separated(out, words_str))
    /* Consequence of the dropped characterisation: the result is no longer than the input. */
    ensures(0 <= result && result <= words_str_len)
{
    long n = 0;
    long i = words_str_len - 1;

    while (i >= 0) invariant(-1 <= i && i < words_str_len && 0 <= n && n <= words_str_len - 1 - i && (n == 0 || i < 0 || words_str[i] == ' ')) {
        while (i >= 0 && words_str[i] == ' ') invariant(-1 <= i && i < words_str_len && n <= words_str_len - 1 - i && (n == 0 || n <= words_str_len - 2 - i || (i >= 0 && words_str[i] == ' '))) {
            i--;
        }
        if (i < 0) {
            break;
        }
        long end = i;

        while (i >= 0 && words_str[i] != ' ') invariant(-1 <= i && i <= end) {
            i--;
        }
        if (n > 0) {
            out[n] = ' ';
            n++;
        }
        for (long j = i + 1; j <= end; j++) invariant(i + 1 <= j && j <= end + 1 && 0 <= n && n <= words_str_len - 2 - end + j - i && (j == i + 1 || n > 0) && (i < 0 || words_str[i] == ' ')) {
            out[n] = words_str[j];
            n++;
        }
    }
    return n;
}
