#include "pfc.h"

/* Verina verina_basic_99: three times x. */
long Triple(long x)
    ensures(result / 3 == x && result / 3 * 3 == result)
{
    return 3 * x;
}
