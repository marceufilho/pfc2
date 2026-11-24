#include "pfc.h"

/* Verina verina_advanced_66: the words of the string in reverse order, separated by single spaces; returns the
 * length of the result. */
long reverseWords(long words_str_len, const char words_str[words_str_len], long out_cap, char out[out_cap])
    requires(out_cap >= words_str_len)
{
    long n = 0;
    long i = words_str_len - 1;

    while (i >= 0) {
        while (i >= 0 && words_str[i] == ' ') {
            i--;
        }
        if (i < 0) {
            break;
        }
        long end = i;

        while (i >= 0 && words_str[i] != ' ') {
            i--;
        }
        if (n > 0) {
            out[n] = ' ';
            n++;
        }
        for (long j = i + 1; j <= end; j++) {
            out[n] = words_str[j];
            n++;
        }
    }
    return n;
}
