#include "pfc.h"

/* Verina verina_basic_11: the last decimal digit of a non-negative n. */
long lastDigit(long n)
    requires(n >= 0)
    ensures(0 <= result && result < 10)
    ensures(result == n % 10)
{
    return n % 10;
}
