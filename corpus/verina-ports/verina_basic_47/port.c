#include "pfc.h"

/* Verina verina_basic_47: sum of the elements of a. */
long arraySum(long a_len, const long a[a_len])
{
    long sum = 0;

    for (long i = 0; i < a_len; i++) {
        sum += a[i];
    }
    return sum;
}
