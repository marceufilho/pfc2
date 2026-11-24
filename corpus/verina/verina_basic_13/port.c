#include "pfc.h"

/* Verina verina_basic_13: the cube of every element of a. */
long cubeElements(long a_len, const long a[a_len], long out_cap, long out[out_cap])
    requires(out_cap >= a_len)
    ensures(result == a_len)
{
    for (long i = 0; i < a_len; i++) invariant(0 <= i) {
        out[i] = a[i] * a[i] * a[i];
    }
    return a_len;
}
