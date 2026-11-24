#include "pfc.h"

/* Verina verina_basic_86: a rotated left by offset: out[i] = a[(i + offset) mod n]; returns the length. */
long rotate(long a_len, const long a[a_len], long offset, long out_cap, long out[out_cap])
    requires(offset >= 0)
    requires(out_cap >= a_len)
{
    for (long i = 0; i < a_len; i++) {
        out[i] = a[(i + offset) % a_len];
    }
    return a_len;
}
