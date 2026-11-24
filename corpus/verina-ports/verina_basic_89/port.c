#include "pfc.h"

/* Verina verina_basic_89: s without duplicates, in order of first occurrence, written to out; returns the new length. */
long SetToSeq(long s_len, const long s[s_len], long out_cap, long out[out_cap])
    requires(out_cap >= s_len)
{
    long count = 0;

    for (long i = 0; i < s_len; i++) {
        long seen = 0;

        for (long j = 0; j < count; j++) {
            if (out[j] == s[i]) {
                seen = 1;
                break;
            }
        }
        if (seen == 0) {
            out[count] = s[i];
            count++;
        }
    }
    return count;
}
