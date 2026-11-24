#include "pfc.h"

/* Verina verina_basic_79: out[0] = maximum of a[0..x-1]; out[1] = first index from x on whose element exceeds it, or the last index. */
long onlineMax(long a_len, const long a[a_len], long x, long out_cap, long out[out_cap])
    requires(1 <= x && x < a_len)
    requires(out_cap >= 2)
    requires(separated(out, a))
    ensures(x <= out[1] && out[1] < a_len)
    ensures(a[out[1]] > out[0] || out[1] == a_len - 1)
{
    long m = a[0];
    long p = a_len - 1;

    for (long i = 1; i < x; i++) {
        if (a[i] > m) {
            m = a[i];
        }
    }
    for (long i = x; i < a_len; i++) invariant(x <= i && i <= a_len && p == a_len - 1) {
        if (a[i] > m) {
            p = i;
            break;
        }
    }
    out[0] = m;
    out[1] = p;
    return 0;
}
