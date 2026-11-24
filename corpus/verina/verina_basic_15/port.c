#include "pfc.h"

/* Verina verina_basic_15: 1 when some element plus one equals the next element, else 0. */
long containsConsecutiveNumbers(long a_len, const long a[a_len])
    ensures(result == 0 || result == 1)
{
    for (long i = 0; i + 1 < a_len; i++) invariant(0 <= i && (i == 0 || i < a_len)) {
        if (a[i] + 1 == a[i + 1]) {
            return 1;
        }
    }
    return 0;
}
