#include "pfc.h"

/* Verina verina_advanced_49: merge two ascending arrays into one ascending array in out; returns its length. */
long mergeSortedLists(long arr1_len, const long arr1[arr1_len], long arr2_len, const long arr2[arr2_len], long out_cap, long out[out_cap])
    requires(0 <= arr1_len)
    requires(0 <= arr2_len)
    requires(out_cap >= arr1_len + arr2_len)
    /* Consequence of the dropped permutation: the result has every element of both inputs. */
    ensures(result == arr1_len + arr2_len)
{
    long i = 0;
    long j = 0;
    long k = 0;

    while (i < arr1_len && j < arr2_len) invariant(0 <= i && i <= arr1_len && 0 <= j && j <= arr2_len && k == i + j) {
        if (arr1[i] <= arr2[j]) {
            out[k] = arr1[i];
            i++;
        } else {
            out[k] = arr2[j];
            j++;
        }
        k++;
    }
    while (i < arr1_len) invariant(0 <= i && i <= arr1_len && 0 <= j && j <= arr2_len && k == i + j) decreases(arr1_len - i) {
        out[k] = arr1[i];
        i++;
        k++;
    }
    while (j < arr2_len) invariant(i == arr1_len && 0 <= j && j <= arr2_len && k == i + j) decreases(arr2_len - j) {
        out[k] = arr2[j];
        j++;
        k++;
    }
    return k;
}
