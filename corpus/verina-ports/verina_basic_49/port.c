#include "pfc.h"

/* Verina verina_basic_49: out[0] = 1 and out[1] = index of the first odd number of a, or out[0] = 0 and out[1] = -1. */
long findFirstOdd(long a_len, const long a[a_len], long out_cap, long out[out_cap])
    requires(out_cap >= 2)
{
    out[0] = 0;
    out[1] = -1;
    for (long i = 0; i < a_len; i++) {
        if (a[i] % 2 != 0) {
            out[0] = 1;
            out[1] = i;
            break;
        }
    }
    return 0;
}
