#include "pfc.h"

/* Verina verina_basic_27: out[0] = 1 and out[1] = the first character seen a second time, or out[0] = 0. */
long findFirstRepeatedChar(long s_len, const char s[s_len], long out_cap, long out[out_cap])
    requires(out_cap >= 2)
    ensures(out[0] == 0 || out[0] == 1)
{
    for (long i = 1; i < s_len; i++) invariant(1 <= i) {
        for (long j = 0; j < i; j++) invariant(0 <= j && j <= i) {
            if (s[j] == s[i]) {
                out[0] = 1;
                out[1] = s[i];
                return 0;
            }
        }
    }
    out[0] = 0;
    out[1] = 0;
    return 0;
}
