#include "pfc.h"

/* Verina verina_basic_48: 1 when n is a perfect square, else 0. */
long isPerfectSquare(long n)
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
