#include "pfc.h"

/* Verina verina_basic_35: arr with its zeroes moved to the end, non-zero order kept; returns the length. */
long MoveZeroesToEnd(long arr_len, const long arr[arr_len], long out_cap, long out[out_cap])
    requires(out_cap >= arr_len)
{
    long count = 0;

    for (long i = 0; i < arr_len; i++) {
        if (arr[i] != 0) {
            out[count] = arr[i];
            count++;
        }
    }
    while (count < arr_len) {
        out[count] = 0;
        count++;
    }
    return arr_len;
}
