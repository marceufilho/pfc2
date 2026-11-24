#include "pfc.h"
/* pfc-heldout-6c75d46f2c625eebe978d4882b389d49 */

long init_2_n_u(long A[], long A_len, long m, long n, long C)
{
    REQUIRES(0 <= m && 0 < n && m <= A_len / n);
    long i = 0;
    long j = 0;
    i = 0;
    while (i < m) {
        j = 0;
        while (j < n) {
            A[i * n + j] = C;
            j = j + 1;
        }
        i = i + 1;
    }
    return i;
}
