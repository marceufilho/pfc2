#include "pfc.h"

/* Verina verina_basic_43: sum of the fourth powers of the first n odd natural numbers. */
long sumOfFourthPowerOfOddNumbers(long n)
    requires(n >= 0)
    ensures(15 * result == n * (2 * n + 1) * (7 + 24 * n * n * n - 12 * n * n - 14 * n))
{
    long sum = 0;

    for (long i = 0; i < n; i++) invariant(0 <= i && i <= n && 15 * sum == i * (2 * i + 1) * (7 + 24 * i * i * i - 12 * i * i - 14 * i)) decreases(n - i) {
        long odd = 2 * i + 1;

        sum += odd * odd * odd * odd;
    }
    return sum;
}
