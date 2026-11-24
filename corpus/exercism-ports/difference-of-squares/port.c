#include "pfc.h"

/* Upstream `unsigned int` becomes `long` (P1). */
long squares_sum(long number)
{
    long sum = 0;

    for (long i = 0; i <= number; i++) {
        sum += i * i;
    }
    return sum;
}

long sum_squared(long number)
{
    long sum = 0;

    for (long i = 0; i <= number; i++) {
        sum += i;
    }
    return (sum * sum);
}

long squares_difference(long number)
{
    return (sum_squared(number) - squares_sum(number));
}
