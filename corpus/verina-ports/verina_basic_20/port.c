#include "pfc.h"

/* Verina verina_basic_20: the product of the distinct values of arr (1 for an empty array). */
long uniqueProduct(long arr_len, const long arr[arr_len])
{
    long product = 1;

    for (long i = 0; i < arr_len; i++) {
        _Bool seen = 0;

        for (long j = 0; j < i; j++) {
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
