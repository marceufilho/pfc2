#include "pfc.h"
/* pfc-heldout-142c5eb1496f315f65686d0ac4dbb32d */

long add_3_n_u(const long A[], long A_len, const long B[], long B_len, long C[], long C_len, long m, long n, long p)
{
    REQUIRES(0 <= m && 0 < n && 0 < p && m <= A_len / p / n && m <= B_len / p / n && m <= C_len / p / n);
    long i = 0;
    long j = 0;
    long k = 0;
    i = 0;
    while (i < m) {
        j = 0;
        while (j < n) {
            k = 0;
            while (k < p) {
                C[(i * n + j) * p + k] = A[(i * n + j) * p + k] + B[(i * n + j) * p + k];
                k = k + 1;
            }
            j = j + 1;
        }
        i = i + 1;
    }
    return i;
}
