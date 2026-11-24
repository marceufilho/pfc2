#include "pfc.h"

/* Upstream calls pow(10, e) from <math.h> on integers; the port multiplies (P9). */
long power(long base, long exponent)
    requires(base == 10 && 0 <= exponent && exponent <= 9)
    ensures(0 <= result && result <= 1000000000)
    ensures((exponent != 0 || result == 1) && (exponent != 1 || result == 10) && (exponent != 2 || result == 100) && (exponent != 3 || result == 1000) && (exponent != 4 || result == 10000) && (exponent != 5 || result == 100000) && (exponent != 6 || result == 1000000) && (exponent != 7 || result == 10000000) && (exponent != 8 || result == 100000000) && (exponent != 9 || result == 1000000000))
{
    long value = 1;

    for (long i = 0; i < exponent; i++) invariant(0 <= i && i <= exponent && (i != 0 || value == 1) && (i != 1 || value == 10) && (i != 2 || value == 100) && (i != 3 || value == 1000) && (i != 4 || value == 10000) && (i != 5 || value == 100000) && (i != 6 || value == 1000000) && (i != 7 || value == 10000000) && (i != 8 || value == 100000000) && (i != 9 || value == 1000000000)) {
        value = value * base;
    }
    return value;
}

/* The result struct {value, unit} is written to `resistor` (P3, P5): resistor[0] the value, resistor[1] the
 * unit. The enum values arrive as `int` elements. */
long trio_code(long n, const int colors[n], long m, long resistor[m])
    requires(3 <= n && 2 <= m)
    requires(0 <= colors[0] && colors[0] <= 9 && 0 <= colors[1] && colors[1] <= 9 && 0 <= colors[2] && colors[2] <= 9)
    ensures(0 <= resistor[0] && resistor[0] < 1000 && 0 <= resistor[1] && resistor[1] <= 3)
{
    resistor[0] = 0;
    resistor[1] = 0;
    long digits = colors[0] * 10 + colors[1];
    long exponent = colors[2];
    long total = power(10, exponent) * digits;

    while (total / 1000 >= 1) invariant(0 <= total && 0 <= resistor[1] && resistor[1] <= 3 && (resistor[1] != 0 || total <= 99000000000) && (resistor[1] != 1 || total <= 99000000) && (resistor[1] != 2 || total <= 99000) && (resistor[1] != 3 || total <= 99)) {
        ++resistor[1];
        total /= 1000;
    }
    resistor[0] = total;
    return 0;
}
