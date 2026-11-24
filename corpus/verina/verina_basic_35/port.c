#include "pfc.h"

/* Verina verina_basic_35: arr with its zeroes moved to the end, non-zero order kept; returns the length. */
long MoveZeroesToEnd(long arr_len, const long arr[arr_len], long out_cap, long out[out_cap])
    requires(arr_len >= 0) /* a length; this spelling of the parameter does not give the checker 0 <= arr_len */
    requires(out_cap >= arr_len)
    ensures(result == arr_len)
{
    long count = 0;

    for (long i = 0; i < arr_len; i++) invariant(0 <= i && i <= arr_len && 0 <= count && count <= i) decreases(arr_len - i) {
        if (arr[i] != 0) {
            out[count] = arr[i];
            count++;
        }
    }
    while (count < arr_len) invariant(0 <= count && count <= arr_len) decreases(arr_len - count) {
        out[count] = 0;
        count++;
    }
    return arr_len;
}
