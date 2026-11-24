#include "pfc.h"

/* Verina verina_advanced_20: 1 when n is divisible by 8 or has 8 among its decimal digits, else 0. */
long isItEight(long n)
{
    if (n % 8 == 0) {
        return 1;
    }
    long rest = n;
    while (rest != 0) {
        long digit = rest % 10;
        if (digit == 8 || digit == -8) {
            return 1;
        }
        rest = rest / 10;
    }
    return 0;
}
