#include "pfc.h"

/* Verina verina_basic_37: index of the first occurrence of target in a sorted array, or -1. */
long findFirstOccurrence(long arr_len, const long arr[arr_len], long target)
    requires(arr_len >= 0) /* a length; this spelling of the parameter does not give the checker 0 <= arr_len */
    ensures(result == -1 || (0 <= result && result < arr_len && arr[result] == target))
{
    for (long i = 0; i < arr_len; i++) invariant(0 <= i && i <= arr_len) {
        if (arr[i] == target) {
            return i;
        }
        if (arr[i] > target) {
            break;
        }
    }
    return -1;
}
