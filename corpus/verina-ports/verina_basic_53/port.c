#include "pfc.h"

/* Verina verina_basic_53: sum of the first N natural numbers. */
long CalSum(long N)
{
    long sum = 0;

    for (long i = 1; i <= N; i++) {
        sum += i;
    }
    return sum;
}
