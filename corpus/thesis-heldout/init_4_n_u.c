#include "pfc.h"
/* pfc-heldout-bdac8dafafb06881dc74dc4a1745c936 */

long init_4_n_u(long A[], long A_len, long m, long n, long p, long q, long C)
{
    REQUIRES(0 <= m && 0 < n && 0 < p && 0 < q && m <= A_len / q / p / n);
    long i = 0;
    long j = 0;
    long k = 0;
    long l = 0;
    i = 0;
    while (i < m) {
        j = 0;
        while (j < n) {
            k = 0;
            while (k < p) {
                l = 0;
                while (l < q) {
                    A[((i * n + j) * p + k) * q + l] = C;
                    l = l + 1;
                }
                k = k + 1;
            }
            j = j + 1;
        }
        i = i + 1;
    }
    return i;
}
