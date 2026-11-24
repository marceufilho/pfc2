#include "pfc.h"
/* pfc-heldout-b43f137840ac2086310cde574fe49c38 */

long rev_3_u(long A[], long A_len, const long B[], long B_len, long n)
{
    REQUIRES(0 < n && n <= A_len / n / n && n <= B_len / n / n);
    long i = 0;
    long j = 0;
    long k = 0;
    i = 0;
    while (i < n) {
        j = 0;
        while (j < n) {
            k = 0;
            while (k < n) {
                A[(i * n + j) * n + k] = B[((n - i - 1) * n + (n - j - 1)) * n + (n - k - 1)];
                k = k + 1;
            }
            j = j + 1;
        }
        i = i + 1;
    }
    return i;
}
