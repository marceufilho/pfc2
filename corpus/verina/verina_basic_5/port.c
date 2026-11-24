#include "pfc.h"

/* Verina verina_basic_5: product of a and b. */
long multiply(long a, long b)
    ensures(result == a * b)
{
    return a * b;
}
