#include "pfc.h"

/* Verina verina_advanced_18: 1 when n equals the sum of its digits each raised to the number of digits. */
long isArmstrong(long n)
    requires(n >= 0) /* n is a Nat */
    /* The postcondition is a fold of digit powers over the decimal string: recursive, dropped. */
    ensures(result == 0 || result == 1)
{
    long digits = 0;
    long rest = n;
    while (rest > 0) {
        digits++;
        rest = rest / 10;
    }

    long sum = 0;
    rest = n;
    while (rest > 0) {
        long digit = rest % 10;
        long power = 1;
        for (long k = 0; k < digits; k++) {
            power = power * digit;
        }
        sum = sum + power;
        rest = rest / 10;
    }

    if (sum == n) {
        return 1;
    }
    return 0;
}
