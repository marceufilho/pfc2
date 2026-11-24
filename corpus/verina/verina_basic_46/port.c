#include "pfc.h"

/* Verina verina_basic_46: index of the last occurrence of elem in a sorted array, or -1. */
long lastPosition(long arr_len, const long arr[arr_len], long elem)
    requires(arr_len >= 0)
    ensures(result == -1 || (0 <= result && result < arr_len && arr[result] == elem))
{
    for (long i = arr_len - 1; i >= 0; i--) {
        if (arr[i] == elem) {
            return i;
        }
    }
    return -1;
}
