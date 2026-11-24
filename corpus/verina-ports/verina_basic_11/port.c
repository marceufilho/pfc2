#include "pfc.h"

/* Verina verina_basic_11: the last decimal digit of a non-negative n. */
long lastDigit(long n)
    requires(n >= 0)
{
    return n % 10;
}
