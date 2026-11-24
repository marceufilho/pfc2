#include "pfc.h"

/* Verina verina_basic_10: 1 when n is strictly greater than every element of a, else 0. */
long isGreater(long n, long a_len, const long a[a_len])
{
    for (long i = 0; i < a_len; i++) {
        if (n <= a[i]) {
            return 0;
        }
    }
    return 1;
}
