#include "pfc.h"

/* Verina verina_advanced_73: the smallest natural number absent from an increasingly sorted list. */
long smallestMissing(long l_len, const long l[l_len])
{
    long expected = 0;

    for (long i = 0; i < l_len; i++) {
        if (l[i] == expected) {
            expected++;
        } else if (l[i] > expected) {
            break;
        }
    }
    return expected;
}
