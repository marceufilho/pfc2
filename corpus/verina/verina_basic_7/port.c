#include "pfc.h"

/* Verina verina_basic_7: sum of the squares of the first n odd natural numbers, by the closed formula. */
long sumOfSquaresOfFirstNOddNumbers(long n)
    requires(n >= 0)
    ensures(result == (n * (2 * n - 1) * (2 * n + 1)) / 3)
{
    return (n * (2 * n - 1) * (2 * n + 1)) / 3;
}
