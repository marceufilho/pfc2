#include "pfc.h"

/* Verina verina_basic_4: the kth element of arr, counting from 1. */
long kthElement(long arr_len, const long arr[arr_len], long k)
    requires(1 <= k && k <= arr_len)
    ensures(result == arr[k - 1])
{
    return arr[k - 1];
}
