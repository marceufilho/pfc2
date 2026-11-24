#include "pfc.h"

/* Verina verina_basic_100: three times x. */
long Triple(long x)
    ensures(result / 3 == x && result / 3 * 3 == result)
{
    if (x == 0) {
        return 0;
    }
    return x + 2 * x;
}
