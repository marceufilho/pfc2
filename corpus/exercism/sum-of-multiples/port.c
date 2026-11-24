#include "pfc.h"

/* Sum of the numbers below `limit` that are multiples of a factor. `unsigned int` becomes `long` (P1, P4);
 * upstream's test for a NULL array stays in the host glue. */
long multiples_sum(long n, const long factors[n], long limit)
    requires(limit <= 2147483647)
    ensures(0 <= result)
    ensures(limit > 1 || result == 0)
    ensures(n != 0 || result == 0)
    ensures(limit < 1 || 2 * result <= limit * (limit - 1))
{
    long sum = 0;

    for (long current = 1; current < limit; current++) invariant(1 <= current && (current <= limit || limit < 1) && 0 <= sum && 2 * sum <= current * (current - 1) && (n != 0 || sum == 0) && (limit > 1 || sum == 0)) {
        for (long i = 0; i < n; i++) invariant(0 <= i && i <= n && 0 <= sum && 2 * sum <= current * (current - 1) && (n != 0 || sum == 0) && (limit > 1 || sum == 0)) {
            if (0 != factors[i] && (current % factors[i]) == 0) {
                sum += current;
                break;
            }
        }
    }
    return sum;
}
