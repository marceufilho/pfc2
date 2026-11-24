#include "pfc.h"

/* Verina verina_advanced_64: the elements of lst different from target, in order; returns their count. */
long removeElement(long lst_len, const long lst[lst_len], long target, long out_cap, long out[out_cap])
    requires(out_cap >= lst_len)
{
    long k = 0;

    for (long i = 0; i < lst_len; i++) {
        if (lst[i] != target) {
            out[k] = lst[i];
            k++;
        }
    }
    return k;
}
