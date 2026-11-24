#include "pfc.h"
/* pfc-heldout-463bb01e4bbc5ad1668e1b7ab36bc689 */

long init_non_constant_3_u(long A[], long A_len, long n, long C)
{
    REQUIRES(0 < n && n <= A_len / n / n);
    long i = 0;
    long j = 0;
    long k = 0;
    i = 0;
    while (i < n) {
        j = 0;
        while (j < n) {
            k = 0;
            while (k < n) {
                A[(i * n + j) * n + k] = i + j + k + C;
                k = k + 1;
            }
            j = j + 1;
        }
        i = i + 1;
    }
    return i;
}
