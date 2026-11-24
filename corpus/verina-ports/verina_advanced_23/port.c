#include "pfc.h"

/* Verina verina_advanced_23: 1 when n is a power of two (n > 0), else 0. */
long isPowerOfTwo(long n)
{
    if (n <= 0) {
        return 0;
    }
    while (n % 2 == 0) {
        n = n / 2;
    }
    if (n == 1) {
        return 1;
    }
    return 0;
}
