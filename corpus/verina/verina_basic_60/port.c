#include "pfc.h"

/* Verina verina_basic_60: the even numbers of arr, in order, written to out; returns how many. */
long FindEvenNumbers(long arr_len, const long arr[arr_len], long out_cap, long out[out_cap])
    requires(out_cap >= arr_len)
{
    long count = 0;

    for (long i = 0; i < arr_len; i++) invariant(0 <= count && count <= i) {
        if (arr[i] % 2 == 0) {
            out[count] = arr[i];
            count++;
        }
    }
    return count;
}
