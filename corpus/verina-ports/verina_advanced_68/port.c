#include "pfc.h"

/* Verina verina_advanced_68: run-length encoding: each run of equal characters becomes the character followed
 * by the decimal length of the run; returns the length of the result. */
long runLengthEncoder(long input_len, const char input[input_len], long out_cap, char out[out_cap])
    requires(out_cap >= 2 * input_len)
{
    long digits[20] = {0};
    long n = 0;
    long i = 0;

    while (i < input_len) {
        long j = i;

        while (j < input_len && input[j] == input[i]) {
            j++;
        }
        out[n] = input[i];
        n++;
        long count = j - i;
        long d = 0;

        while (count > 0) {
            digits[d] = count % 10;
            count /= 10;
            d++;
        }
        while (d > 0) {
            d--;
            out[n] = '0' + digits[d];
            n++;
        }
        i = j;
    }
    return n;
}
