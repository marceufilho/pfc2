#include "pfc.h"

/* Verina verina_basic_2: the smallest element of s as an option: out[0] = 1 and out[1] = value, or out[0] = 0. */
long findSmallest(long s_len, const long s[s_len], long out_cap, long out[out_cap])
    requires(out_cap >= 2)
{
    if (s_len == 0) {
        out[0] = 0;
        return 0;
    }
    long smallest = s[0];

    for (long i = 1; i < s_len; i++) {
        if (s[i] < smallest) {
            smallest = s[i];
        }
    }
    out[0] = 1;
    out[1] = smallest;
    return 0;
}
