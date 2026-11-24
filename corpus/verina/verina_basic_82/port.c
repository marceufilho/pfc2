#include "pfc.h"

/* Verina verina_basic_82: a without its first element, written to out; returns the new length. */
long remove_front(long a_len, const long a[a_len], long out_cap, long out[out_cap])
    requires(a_len >= 1)
    requires(out_cap >= a_len - 1)
    ensures(result == a_len - 1)
{
    for (long i = 1; i < a_len; i++) {
        out[i - 1] = a[i];
    }
    return a_len - 1;
}
