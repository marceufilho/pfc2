#include "pfc.h"

/* Verina verina_basic_41: 1 when a is empty or all its elements are equal, else 0. */
long hasOnlyOneDistinctElement(long a_len, const long a[a_len])
{
    for (long i = 1; i < a_len; i++) {
        if (a[i] != a[0]) {
            return 0;
        }
    }
    return 1;
}
