#include "pfc.h"

/* Verina verina_advanced_9: how many numbers below n have a digit sum divisible by d. */
long countSumDivisibleBy(long n, long d)
    requires(n >= 0)
    requires(d > 0)
{
    long count = 0;

    for (long i = 0; i < n; i++) {
        long sum = 0;
        long rest = i;

        while (rest > 0) {
            sum += rest % 10;
            rest /= 10;
        }
        if (sum % d == 0) {
            count++;
        }
    }
    return count;
}
