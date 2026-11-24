#include "pfc.h"

/* Verina verina_basic_15: 1 when some element plus one equals the next element, else 0. */
long containsConsecutiveNumbers(long a_len, const long a[a_len])
{
    for (long i = 0; i + 1 < a_len; i++) {
        if (a[i] + 1 == a[i + 1]) {
            return 1;
        }
    }
    return 0;
}
