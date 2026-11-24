#include "pfc.h"

/* Verina verina_advanced_23: 1 when n is a power of two (n > 0), else 0. */
long isPowerOfTwo(long n)
    /* result <-> exists x, pow 2 x = n and n > 0: the existential over a recursive power is dropped.
     * Its conjunct n > 0 cannot be stated either: the code overwrites n and an ensures reads the final value. */
    ensures(result == 0 || result == 1)
{
    if (n <= 0) {
        return 0;
    }
    while (n % 2 == 0) invariant(n > 0) {
        n = n / 2;
    }
    if (n == 1) {
        return 1;
    }
    return 0;
}
