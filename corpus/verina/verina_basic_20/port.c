#include "pfc.h"

/* Verina verina_basic_20: the product of the distinct values of arr (1 for an empty array). */
long uniqueProduct(long arr_len, const long arr[arr_len])
    requires(arr_len >= 0) /* a length; this spelling of the parameter does not give the checker 0 <= arr_len */
    ensures(arr_len != 0 || result == 1)
{
    long product = 1;

    for (long i = 0; i < arr_len; i++) invariant(0 <= i && i <= arr_len && (i != 0 || product == 1)) {
        _Bool seen = 0;

        for (long j = 0; j < i; j++) invariant(0 <= j && j <= i) {
            if (arr[j] == arr[i]) {
                seen = 1;
                break;
            }
        }
        if (!seen) {
            product *= arr[i];
        }
    }
    return product;
}
