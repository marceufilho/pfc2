#include "pfc.h"

/* Verina verina_basic_48: 1 when n is a perfect square, else 0. */
long isPerfectSquare(long n)
    requires(n >= 0)
    ensures(result == 0 || result == 1)
{
    long i = 0;

    while (i * i < n) {
        i++;
    }
    if (i * i == n) {
        return 1;
    }
    return 0;
}
