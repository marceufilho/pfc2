#include "pfc.h"

/* Verina verina_advanced_72: the smallest of 2, 3, 5, 7 that divides n, or 0 (also 0 for n = 0). */
long singleDigitPrimeFactor(long n)
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
