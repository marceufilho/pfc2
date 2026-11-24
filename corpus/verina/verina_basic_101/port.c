#include "pfc.h"

/* Verina verina_basic_101: three times x, by doubling and adding. */
long Triple(long x)
    ensures(result / 3 == x && result / 3 * 3 == result)
{
    long twice = 2 * x;

    return twice + x;
}
