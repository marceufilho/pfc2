#include "pfc.h"
/* pfc-heldout-cd7d7d0c362e915988ecf93d3a4001d5 */

long copy_partial_2_n_u(long A[], long A_len, const long B[], long B_len, long m, long n, long q, long s)
{
    REQUIRES(0 <= m && 0 < n && m <= A_len / n && m <= B_len / n && 0 <= q && q < m && 0 <= s && s < n);
    long i = 0;
    long j = 0;
    i = 0;
    while (i < q) {
        j = 0;
        while (j < s) {
            A[i * n + j] = B[i * n + j];
            j = j + 1;
        }
        i = i + 1;
    }
    return i;
}
