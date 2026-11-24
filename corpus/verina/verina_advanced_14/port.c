#include "pfc.h"

/* Verina verina_advanced_14: 1 when n is a power of four, else 0. */
long ifPowerOfFour(long n)
    requires(n >= 0) /* n is a Nat */
    /* result <-> exists m, n = 4^m: an existential over a power, dropped. */
    ensures(result == 0 || result == 1)
{
    if (n <= 0) {
        return 0;
    }
    while (n % 4 == 0) invariant(n > 0) {
        n = n / 4;
    }
    if (n == 1) {
        return 1;
    }
    return 0;
}
