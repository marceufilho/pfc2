#include "pfc.h"

/* Verina verina_basic_100: three times x. */
long Triple(long x)
{
    if (x == 0) {
        return 0;
    }
    return x + 2 * x;
}
