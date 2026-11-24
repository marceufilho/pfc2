#include "pfc.h"

/* Upstream `unsigned int` becomes `long` (P1). */
long squares_sum(long number)
    requires(0 <= number && number <= 1000)
    ensures(6 * result == number * (number + 1) * (2 * number + 1))
{
    long sum = 0;

    for (long i = 0; i <= number; i++) invariant(0 <= i && i <= number + 1 && 6 * sum == (i - 1) * i * (2 * i - 1)) {
        sum += i * i;
    }
    return sum;
}

long sum_squared(long number)
    requires(0 <= number && number <= 1000)
    ensures(4 * result == number * number * (number + 1) * (number + 1))
{
    long sum = 0;

    for (long i = 0; i <= number; i++) invariant(0 <= i && i <= number + 1 && 2 * sum == (i - 1) * i) {
        sum += i;
    }
    return (sum * sum);
}

long squares_difference(long number)
    requires(0 <= number && number <= 1000)
    ensures(12 * result == 3 * number * number * (number + 1) * (number + 1) - 2 * number * (number + 1) * (2 * number + 1))
{
    return (sum_squared(number) - squares_sum(number));
}
