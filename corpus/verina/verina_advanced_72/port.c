#include "pfc.h"

/* Verina verina_advanced_72: the smallest of 2, 3, 5, 7 that divides n, or 0 (also 0 for n = 0). */
long singleDigitPrimeFactor(long n)
    requires(0 <= n)
    ensures(result == 0 || result == 2 || result == 3 || result == 5 || result == 7)
    ensures(result != 0 || n == 0 || (n % 2 != 0 && n % 3 != 0 && n % 5 != 0 && n % 7 != 0))
    ensures(result == 0 || (n != 0 && n % result == 0))
    /* "No x below result that is one of 2, 3, 5, 7 divides n", unfolded over the four literals. */
    ensures(result == 0 || ((result <= 2 || n % 2 != 0) && (result <= 3 || n % 3 != 0) && (result <= 5 || n % 5 != 0) && (result <= 7 || n % 7 != 0)))
{
    if (n == 0) {
        return 0;
    }
    if (n % 2 == 0) {
        return 2;
    }
    if (n % 3 == 0) {
        return 3;
    }
    if (n % 5 == 0) {
        return 5;
    }
    if (n % 7 == 0) {
        return 7;
    }
    return 0;
}
