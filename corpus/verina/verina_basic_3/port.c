#include "pfc.h"

/* Verina verina_basic_3: 1 when n is divisible by 11, else 0. */
long isDivisibleBy11(long n)
    ensures((result == 1 && n % 11 == 0) || (result == 0 && n % 11 != 0))
{
    if (n % 11 == 0) {
        return 1;
    }
    return 0;
}
