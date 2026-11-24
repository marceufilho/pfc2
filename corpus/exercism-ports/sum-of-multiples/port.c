#include "pfc.h"

/* Sum of the numbers below `limit` that are multiples of a factor. `unsigned int` becomes `long` (P1, P4);
 * upstream's test for a NULL array stays in the host glue. */
long multiples_sum(long n, const long factors[n], long limit)
{
    long sum = 0;

    for (long current = 1; current < limit; current++) {
        for (long i = 0; i < n; i++) {
            if (0 != factors[i] && (current % factors[i]) == 0) {
                sum += current;
                break;
            }
        }
    }
    return sum;
}
