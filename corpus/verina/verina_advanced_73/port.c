#include "pfc.h"

/* Verina verina_advanced_73: the smallest natural number absent from an increasingly sorted list. */
long smallestMissing(long l_len, const long l[l_len])
    requires(0 <= l_len)
    /* Consequence of the dropped "every natural below result occurs in l" for a list without repeats. */
    ensures(0 <= result && result <= l_len)
{
    long expected = 0;

    for (long i = 0; i < l_len; i++) invariant(0 <= i && i <= l_len && 0 <= expected && expected <= i) {
        if (l[i] == expected) {
            expected++;
        } else if (l[i] > expected) {
            break;
        }
    }
    return expected;
}
