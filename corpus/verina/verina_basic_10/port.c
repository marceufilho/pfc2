#include "pfc.h"

/* Verina verina_basic_10: 1 when n is strictly greater than every element of a, else 0. */
long isGreater(long n, long a_len, const long a[a_len])
    requires(a_len > 0)
    ensures(result == 0 || result == 1)
{
    for (long i = 0; i < a_len; i++) invariant(0 <= i) {
        if (n <= a[i]) {
            return 0;
        }
    }
    return 1;
}
