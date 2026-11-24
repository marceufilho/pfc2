#include "pfc.h"
/* pfc-heldout-f57c05472512c431214a006970421633 */

long rev_2_n_u(long A[], long A_len, const long B[], long B_len, long m, long n)
{
    REQUIRES(0 <= m && 0 < n && m <= A_len / n && m <= B_len / n);
    long i = 0;
    long j = 0;
    i = 0;
    while (i < m) {
        j = 0;
        while (j < n) {
            A[i * n + j] = B[(m - i - 1) * n + (n - j - 1)];
            j = j + 1;
        }
        i = i + 1;
    }
    return i;
}
