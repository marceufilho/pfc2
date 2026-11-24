#include "pfc.h"

/* Verina verina_basic_103: a copy of a with element 4 increased by 3 and element 7 set to 516. */
long UpdateElements(long a_len, const long a[a_len], long out_cap, long out[out_cap])
    requires(a_len >= 8)
    requires(out_cap >= a_len)
    requires(separated(out, a))
    ensures(result == a_len)
    ensures(out[4] == a[4] + 3)
    ensures(out[7] == 516)
{
    for (long i = 0; i < a_len; i++) invariant(0 <= i) {
        out[i] = a[i];
    }
    out[4] = a[4] + 3;
    out[7] = 516;
    return a_len;
}
