#include "pfc.h"

/* Verina verina_basic_43: sum of the fourth powers of the first n odd natural numbers. */
long sumOfFourthPowerOfOddNumbers(long n)
{
    long sum = 0;

    for (long i = 0; i < n; i++) {
        long odd = 2 * i + 1;

        sum += odd * odd * odd * odd;
    }
    return sum;
}
