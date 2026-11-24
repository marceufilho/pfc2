#include "pfc.h"

/* Verina verina_basic_18: the sum of the decimal digits of a non-negative n. */
long sumOfDigits(long n)
    requires(n >= 0)
{
    long sum = 0;
    long rest = n;

    while (rest > 0) {
        sum += rest % 10;
        rest /= 10;
    }
    return sum;
}
