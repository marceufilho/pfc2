#include "pfc.h"

/* Verina verina_basic_32: a copy of a with its first and last elements swapped. */
long swapFirstAndLast(long a_len, const long a[a_len], long out_cap, long out[out_cap])
    requires(a_len >= 1)
    requires(out_cap >= a_len)
    requires(separated(out, a))
    ensures(result == a_len)
    ensures(out[0] == a[a_len - 1])
    ensures(out[result - 1] == a[0])
{
    for (long i = 0; i < a_len; i++) invariant(0 <= i && i <= a_len) decreases(a_len - i) {
        out[i] = a[i];
    }
    out[0] = a[a_len - 1];
    out[a_len - 1] = a[0];
    return a_len;
}
