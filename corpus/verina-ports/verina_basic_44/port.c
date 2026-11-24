#include "pfc.h"

/* Verina verina_basic_44: 1 when every odd index of a holds an odd number, else 0. */
long isOddAtIndexOdd(long a_len, const long a[a_len])
{
    for (long i = 1; i < a_len; i += 2) {
        if (a[i] % 2 == 0) {
            return 0;
        }
    }
    return 1;
}
