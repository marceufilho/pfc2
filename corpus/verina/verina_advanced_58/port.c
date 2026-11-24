#include "pfc.h"

/* Verina verina_advanced_58: the nth (1-based) positive integer whose only prime factors are 2, 3 and 5. */
long is_ugly(long x)
    ensures(result == 0 || result == 1)
{
    long rest = x;

    while (rest % 2 == 0) {
        rest /= 2;
    }
    while (rest % 3 == 0) {
        rest /= 3;
    }
    while (rest % 5 == 0) {
        rest /= 5;
    }
    if (rest == 1) {
        return 1;
    }
    return 0;
}

long nthUglyNumber(long n)
    requires(n > 0)
    /* Consequence of the dropped isUgly(result): zero is not ugly. */
    ensures(result >= 1)
{
    long count = 0;
    long x = 0;

    while (count < n) invariant(0 <= x && 0 <= count && count <= x) {
        x++;
        if (is_ugly(x)) {
            count++;
        }
    }
    return x;
}
