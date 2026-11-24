#include "pfc.h"
/* pfc-heldout-99047e7abe0967e185afe1ed41b70d9e */

long max_2_u(const long A[], long A_len, long n)
{
    REQUIRES(0 < n && n <= A_len / n);
    long i = 0;
    long j = 0;
    long max = A[0];
    i = 0;
    while (i < n) {
        j = 0;
        while (j < n) {
            if (A[i * n + j] > max) {
                max = A[i * n + j];
            }
            j = j + 1;
        }
        i = i + 1;
    }
    return max;
}
