#include "pfc.h"
/* pfc-heldout-12d186ba1c86d56c3e4d40d2454bc5dd */

long copy_partial_3_u(long A[], long A_len, const long B[], long B_len, long n, long p)
{
    REQUIRES(0 < n && n <= A_len / n / n && n <= B_len / n / n && 0 <= p && p < n);
    long i = 0;
    long j = 0;
    long k = 0;
    i = 0;
    while (i < p) {
        j = 0;
        while (j < p) {
            k = 0;
            while (k < p) {
                A[(i * n + j) * n + k] = B[(i * n + j) * n + k];
                k = k + 1;
            }
            j = j + 1;
        }
        i = i + 1;
    }
    i = p;
    while (i < n) {
        j = p;
        while (j < n) {
            k = p;
            while (k < n) {
                A[(i * n + j) * n + k] = B[(i * n + j) * n + k];
                k = k + 1;
            }
            j = j + 1;
        }
        i = i + 1;
    }
    return i;
}
