#include "pfc.h"
/* pfc-heldout-3a782dba7a88ac14c75b14935c9b8943 */

long copy_2_u(long A[], long A_len, const long B[], long B_len, long n)
{
    REQUIRES(0 < n && n <= A_len / n && n <= B_len / n);
    long i = 0;
    long j = 0;
    i = 0;
    while (i < n) {
        j = 0;
        while (j < n) {
            A[i * n + j] = B[i * n + j];
            j = j + 1;
        }
        i = i + 1;
    }
    return i;
}
