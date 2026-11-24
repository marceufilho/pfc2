#include "pfc.h"

/* Verina verina_basic_53: sum of the first N natural numbers. */
long CalSum(long N)
    requires(N >= 0)
    ensures(2 * result == N * (N + 1))
{
    long sum = 0;

    for (long i = 1; i <= N; i++) invariant(1 <= i && i <= N + 1 && 2 * sum == (i - 1) * i) {
        sum += i;
    }
    return sum;
}
