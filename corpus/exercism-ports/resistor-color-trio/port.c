#include "pfc.h"

/* Upstream calls pow(10, e) from <math.h> on integers; the port multiplies (P9). */
long power(long base, long exponent)
{
    long value = 1;

    for (long i = 0; i < exponent; i++) {
        value = value * base;
    }
    return value;
}

/* The result struct {value, unit} is written to `resistor` (P3, P5): resistor[0] the value, resistor[1] the
 * unit. The enum values arrive as `int` elements. */
long trio_code(long n, const int colors[n], long m, long resistor[m])
{
    resistor[0] = 0;
    resistor[1] = 0;
    long digits = colors[0] * 10 + colors[1];
    long exponent = colors[2];
    long total = power(10, exponent) * digits;

    while (total / 1000 >= 1) {
        ++resistor[1];
        total /= 1000;
    }
    resistor[0] = total;
    return 0;
}
