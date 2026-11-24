#include "pfc.h"
/* pfc-heldout-3e71a7c2e379bfd37e42dee439b0b243 */

long min_3_n_u(const long A[], long A_len, long m, long n, long p)
{
    REQUIRES(0 < m && 0 < n && 0 < p && m <= A_len / p / n);
    long i = 0;
    long j = 0;
    long k = 0;
    long min = A[0];
    i = 0;
    while (i < m) {
        j = 0;
        while (j < n) {
            k = 0;
            while (k < p) {
                if (A[(i * n + j) * p + k] < min) {
                    min = A[(i * n + j) * p + k];
                }
                k = k + 1;
            }
            j = j + 1;
        }
        i = i + 1;
    }
    return min;
}
