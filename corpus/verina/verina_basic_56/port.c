#include "pfc.h"

/* Verina verina_basic_56: dest with dest[dStart .. dStart+len-1] replaced by src[sStart .. sStart+len-1], written to out; returns the length. */
long copy(long src_len, const long src[src_len], long sStart, long dest_len, const long dest[dest_len], long dStart,
          long len, long out_cap, long out[out_cap])
    requires(sStart >= 0)
    requires(dStart >= 0)
    requires(len >= 0)
    requires(sStart + len <= src_len)
    requires(dStart + len <= dest_len)
    requires(out_cap >= dest_len)
    ensures(result == dest_len)
{
    for (long i = 0; i < dest_len; i++) {
        out[i] = dest[i];
    }
    for (long i = 0; i < len; i++) {
        out[dStart + i] = src[sStart + i];
    }
    return dest_len;
}
