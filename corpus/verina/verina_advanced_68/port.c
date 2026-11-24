#include "pfc.h"

/* Verina verina_advanced_68: run-length encoding: each run of equal characters becomes the character followed
 * by the decimal length of the run; returns the length of the result. */
long runLengthEncoder(long input_len, const char input[input_len], long out_cap, char out[out_cap])
    requires(out_cap >= 2 * input_len)
    requires(0 <= input_len)
    ensures((input_len == 0 || result > 0) && (input_len > 0 || result == 0))
{
    long digits[20] = {0};
    long n = 0;
    long i = 0;

    while (i < input_len) invariant(0 <= i && i <= input_len && 0 <= n && n <= 2 * i && (i == 0 || n > 0)) {
        long j = i;

        while (j < input_len && input[j] == input[i]) invariant(i <= j && j <= input_len) {
            j++;
        }
        out[n] = input[i];
        n++;
        long count = j - i;
        long d = 0;

        while (count > 0) invariant(0 <= count && 0 <= d && d <= 19 && d + count <= j - i && (d != 0 || count <= 9223372036854775807) && (d != 1 || count <= 922337203685477580) && (d != 2 || count <= 92233720368547758) && (d != 3 || count <= 9223372036854775) && (d != 4 || count <= 922337203685477) && (d != 5 || count <= 92233720368547) && (d != 6 || count <= 9223372036854) && (d != 7 || count <= 922337203685) && (d != 8 || count <= 92233720368) && (d != 9 || count <= 9223372036) && (d != 10 || count <= 922337203) && (d != 11 || count <= 92233720) && (d != 12 || count <= 9223372) && (d != 13 || count <= 922337) && (d != 14 || count <= 92233) && (d != 15 || count <= 9223) && (d != 16 || count <= 922) && (d != 17 || count <= 92) && (d != 18 || count <= 9) && (d != 19 || count <= 0) && (d <= 0 || digits[0] / 80 == 0) && (d <= 1 || digits[1] / 80 == 0) && (d <= 2 || digits[2] / 80 == 0) && (d <= 3 || digits[3] / 80 == 0) && (d <= 4 || digits[4] / 80 == 0) && (d <= 5 || digits[5] / 80 == 0) && (d <= 6 || digits[6] / 80 == 0) && (d <= 7 || digits[7] / 80 == 0) && (d <= 8 || digits[8] / 80 == 0) && (d <= 9 || digits[9] / 80 == 0) && (d <= 10 || digits[10] / 80 == 0) && (d <= 11 || digits[11] / 80 == 0) && (d <= 12 || digits[12] / 80 == 0) && (d <= 13 || digits[13] / 80 == 0) && (d <= 14 || digits[14] / 80 == 0) && (d <= 15 || digits[15] / 80 == 0) && (d <= 16 || digits[16] / 80 == 0) && (d <= 17 || digits[17] / 80 == 0) && (d <= 18 || digits[18] / 80 == 0)) {
            digits[d] = count % 10;
            count /= 10;
            d++;
        }
        while (d > 0) invariant(0 <= d && d <= 19 && 0 < n && n + d <= i + j + 1 && (d <= 0 || digits[0] / 80 == 0) && (d <= 1 || digits[1] / 80 == 0) && (d <= 2 || digits[2] / 80 == 0) && (d <= 3 || digits[3] / 80 == 0) && (d <= 4 || digits[4] / 80 == 0) && (d <= 5 || digits[5] / 80 == 0) && (d <= 6 || digits[6] / 80 == 0) && (d <= 7 || digits[7] / 80 == 0) && (d <= 8 || digits[8] / 80 == 0) && (d <= 9 || digits[9] / 80 == 0) && (d <= 10 || digits[10] / 80 == 0) && (d <= 11 || digits[11] / 80 == 0) && (d <= 12 || digits[12] / 80 == 0) && (d <= 13 || digits[13] / 80 == 0) && (d <= 14 || digits[14] / 80 == 0) && (d <= 15 || digits[15] / 80 == 0) && (d <= 16 || digits[16] / 80 == 0) && (d <= 17 || digits[17] / 80 == 0) && (d <= 18 || digits[18] / 80 == 0)) {
            d--;
            out[n] = '0' + digits[d];
            n++;
        }
        i = j;
    }
    return n;
}
