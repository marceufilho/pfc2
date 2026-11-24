#include "pfc.h"

/* Verina verina_basic_97: copy of a with the element at j set to 60; returns the length. */
long TestArrayElements(long a_len, const long a[a_len], long j, long out_cap, long out[out_cap])
    requires(0 <= j && j < a_len)
    requires(out_cap >= a_len)
    ensures(result == a_len)
    ensures(out[j] == 60)
{
    for (long i = 0; i < a_len; i++) {
        out[i] = a[i];
    }
    out[j] = 60;
    return a_len;
}
