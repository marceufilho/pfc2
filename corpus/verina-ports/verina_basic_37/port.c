#include "pfc.h"

/* Verina verina_basic_37: index of the first occurrence of target in a sorted array, or -1. */
long findFirstOccurrence(long arr_len, const long arr[arr_len], long target)
{
    for (long i = 0; i < arr_len; i++) {
        if (arr[i] == target) {
            return i;
        }
        if (arr[i] > target) {
            break;
        }
    }
    return -1;
}
