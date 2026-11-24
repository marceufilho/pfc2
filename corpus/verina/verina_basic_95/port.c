#include "pfc.h"

/* Verina verina_basic_95: copy of arr with the elements at i and j exchanged; returns the length. */
long swap(long arr_len, const long arr[arr_len], long i, long j, long out_cap, long out[out_cap])
    requires(0 <= i && i < arr_len)
    requires(0 <= j && j < arr_len)
    requires(out_cap >= arr_len)
    requires(separated(out, arr))
    ensures(result == arr_len)
    ensures(out[i] == arr[j] && out[j] == arr[i])
{
    for (long k = 0; k < arr_len; k++) {
        out[k] = arr[k];
    }
    out[i] = arr[j];
    out[j] = arr[i];
    return arr_len;
}
