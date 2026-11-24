#include "pfc.h"

/* Verina verina_basic_34: the even numbers of arr, in order, written to out; returns how many. */
long findEvenNumbers(long arr_len, const long arr[arr_len], long out_cap, long out[out_cap])
    requires(arr_len >= 0) /* a length; this spelling of the parameter does not give the checker 0 <= arr_len */
    requires(out_cap >= arr_len)
    ensures(0 <= result && result <= arr_len)
{
    long count = 0;

    for (long i = 0; i < arr_len; i++) invariant(0 <= i && i <= arr_len && 0 <= count && count <= i) decreases(arr_len - i) {
        if (arr[i] % 2 == 0) {
            out[count] = arr[i];
            count++;
        }
    }
    return count;
}
