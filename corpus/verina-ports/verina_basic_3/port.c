#include "pfc.h"

/* Verina verina_basic_3: 1 when n is divisible by 11, else 0. */
long isDivisibleBy11(long n)
{
    if (n % 11 == 0) {
        return 1;
    }
    return 0;
}
