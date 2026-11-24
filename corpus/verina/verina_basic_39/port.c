#include "pfc.h"

/* Verina verina_basic_39: l rotated to the right by n positions, written to out; returns the length. */
long rotateRight(long l_len, const long l[l_len], long n, long out_cap, long out[out_cap])
    requires(l_len >= 0) /* a length; this spelling of the parameter does not give the checker 0 <= l_len */
    requires(n >= 0)
    requires(out_cap >= l_len)
    ensures(result == l_len)
{
    if (l_len == 0) {
        return 0;
    }
    long shift = n % l_len;

    for (long i = 0; i < l_len; i++) invariant(0 <= i && i <= l_len && 0 <= shift && shift < l_len) decreases(l_len - i) {
        out[(i + shift) % l_len] = l[i];
    }
    return l_len;
}
