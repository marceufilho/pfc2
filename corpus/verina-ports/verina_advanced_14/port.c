#include "pfc.h"

/* Verina verina_advanced_14: 1 when n is a power of four, else 0. */
long ifPowerOfFour(long n)
{
    if (n <= 0) {
        return 0;
    }
    while (n % 4 == 0) {
        n = n / 4;
    }
    if (n == 1) {
        return 1;
    }
    return 0;
}
