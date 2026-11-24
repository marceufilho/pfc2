#include "pfc.h"
/* pfc-heldout-f3f1a5bcca5b2e7086e84a93f968d34c */

long init_3_u(long A[], long A_len, long n, long C)
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
                A[(i * n + j) * n + k] = C;
                k = k + 1;
            }
            j = j + 1;
        }
        i = i + 1;
    }
    return i;
}
