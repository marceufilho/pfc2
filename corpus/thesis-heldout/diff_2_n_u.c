#include "pfc.h"
/* pfc-heldout-c5da98973db29eb9269d6df047a16935 */

long diff_2_n_u(const long A[], long A_len, const long B[], long B_len, long C[], long C_len, long m, long n)
{
    REQUIRES(0 <= m && 0 < n && m <= A_len / n && m <= B_len / n && m <= C_len / n);
    long i = 0;
    long j = 0;
    i = 0;
    while (i < m) {
        j = 0;
        while (j < n) {
            C[i * n + j] = A[i * n + j] - B[i * n + j];
            j = j + 1;
        }
        i = i + 1;
    }
    return i;
}
