#include "pfc.h"
/* pfc-heldout-ca72d44de5996b45c35906d7f88a0197 */

long copy_3_n_u(long A[], long A_len, const long B[], long B_len, long m, long n, long p)
{
    REQUIRES(0 <= m && 0 < n && 0 < p && m <= A_len / p / n && m <= B_len / p / n);
    long i = 0;
    long j = 0;
    long k = 0;
    i = 0;
    while (i < m) {
        j = 0;
        while (j < n) {
            k = 0;
            while (k < p) {
                A[(i * n + j) * p + k] = B[(i * n + j) * p + k];
                k = k + 1;
            }
            j = j + 1;
        }
        i = i + 1;
    }
    return i;
}
