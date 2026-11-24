#include "pfc.h"

/* Hamming distance of two strands, or -1 when their lengths differ. The strings arrive with their lengths
 * (P2, P7 for strlen); upstream's test for NULL stays in the host glue. */
long hamming_distance(long n, const char lhs[n], long m, const char rhs[m])
    ensures(n == m || result == -1)
    ensures(n != m || (0 <= result && result <= n))
{
    long count = -1;

    if (n == m) {
        count = 0;
        long length = n;

        for (long i = 0; i < length; ++i) invariant(0 <= i && i <= length && 0 <= count && count <= i) {
            if (lhs[i] != rhs[i]) {
                ++count;
            }
        }
    }
    return count;
}
