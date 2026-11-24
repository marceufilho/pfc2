#include "pfc.h"

/* Verina verina_basic_64: the first l characters of oline with the first p characters of nl inserted at atPos, written to out; returns l + p. */
long insert(long oline_len, const char oline[oline_len], long l, long nl_len, const char nl[nl_len], long p,
            long atPos, long out_cap, char out[out_cap])
    requires(0 <= atPos && atPos <= l)
    requires(l <= oline_len)
    requires(0 <= p && p <= nl_len)
    requires(out_cap >= l + p)
    ensures(result == l + p)
{
    for (long i = 0; i < atPos; i++) {
        out[i] = oline[i];
    }
    for (long i = 0; i < p; i++) {
        out[atPos + i] = nl[i];
    }
    for (long i = atPos; i < l; i++) {
        out[i + p] = oline[i];
    }
    return l + p;
}
