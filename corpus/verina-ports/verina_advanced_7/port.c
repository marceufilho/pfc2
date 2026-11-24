#include "pfc.h"

/* Verina verina_advanced_7: value of a binary number given as digits, most significant first. */
long binaryToDecimal(long digits_len, const long digits[digits_len])
{
    long value = 0;

    for (long i = 0; i < digits_len; i++) {
        value = value * 2 + digits[i];
    }
    return value;
}
