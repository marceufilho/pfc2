#include "pfc.h"
/* pfc-heldout-a8552d95185ebdbc3f4e8854499b3848 */

long transpose_u(const long A[], long A_len, long C[], long C_len, long n)
{
    REQUIRES(0 < n && n <= A_len / n && n <= C_len / n);
    long i = 0;
    long j = 0;
    i = 0;
    while (i < n) {
        j = 0;
        while (j < n) {
            C[j * n + i] = A[i * n + j];
            j = j + 1;
        }
        i = i + 1;
    }
    return i;
}
