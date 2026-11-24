#include "pfc.h"

/* Verina verina_basic_79: out[0] = maximum of a[0..x-1]; out[1] = first index from x on whose element exceeds it, or the last index. */
long onlineMax(long a_len, const long a[a_len], long x, long out_cap, long out[out_cap])
    requires(1 <= x && x < a_len)
    requires(out_cap >= 2)
{
    long m = a[0];
    long p = a_len - 1;

    for (long i = 1; i < x; i++) {
        if (a[i] > m) {
            m = a[i];
        }
    }
    for (long i = x; i < a_len; i++) {
        if (a[i] > m) {
            p = i;
            break;
        }
    }
    out[0] = m;
    out[1] = p;
    return 0;
}
