#include "pfc.h"
/* pfc-heldout-d39a3e74b1028f3e6b3d211cd496d60a */

long min_2_u(const long A[], long A_len, long n)
{
    REQUIRES(0 < n && n <= A_len / n);
    long i = 0;
    long j = 0;
    long min = A[0];
    i = 0;
    while (i < n) {
        j = 0;
        while (j < n) {
            if (A[i * n + j] < min) {
                min = A[i * n + j];
            }
            j = j + 1;
        }
        i = i + 1;
    }
    return min;
}
