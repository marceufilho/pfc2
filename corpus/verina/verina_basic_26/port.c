#include "pfc.h"

/* Verina verina_basic_26: 1 when n is even, else 0. */
long isEven(long n)
    ensures((result == 1 && n % 2 == 0) || (result == 0 && n % 2 != 0))
{
    if (n % 2 == 0) {
        return 1;
    }
    return 0;
}
