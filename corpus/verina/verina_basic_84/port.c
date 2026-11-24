#include "pfc.h"

/* Verina verina_basic_84: copy of arr with every element greater than k replaced by -1; returns the length. */
long replace(long arr_len, const long arr[arr_len], long k, long out_cap, long out[out_cap])
    requires(out_cap >= arr_len)
    ensures(result == arr_len)
{
    for (long i = 0; i < arr_len; i++) {
        if (arr[i] > k) {
            out[i] = -1;
        } else {
            out[i] = arr[i];
        }
    }
    return arr_len;
}
