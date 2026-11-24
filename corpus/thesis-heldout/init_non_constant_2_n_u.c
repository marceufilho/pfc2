#include "pfc.h"
/* pfc-heldout-4703cf615b684b807af8ddf9f6034169 */

long init_non_constant_2_n_u(long A[], long A_len, long m, long n, long q, long s, long C)
{
    REQUIRES(0 <= m && 0 < n && m <= A_len / n && 0 <= q && q < m && 0 <= s && s < n);
    long i = 0;
    long j = 0;
    i = 0;
    while (i < q) {
        j = 0;
        while (j < s) {
            A[i * n + j] = i + j + C;
            j = j + 1;
        }
        i = i + 1;
    }
    return i;
}
