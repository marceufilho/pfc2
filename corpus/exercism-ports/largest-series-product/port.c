#include "pfc.h"

long to_int(long c)
{
    return c - '0';
}

_Bool is_digit(long c)
{
    return (c >= '0') && (c <= '9');
}

/* Largest product of `span` adjacent digits, or -1. The string arrives with its length (P2, P7); upstream's
 * MAX macro, written with `?:`, is an `if` (P6, P14); an element is read into a local before a call (P13). */
long largest_product_of(long n, const char digits[n], long span)
{
    long digit_count = n;
    long zeros = 0;
    long product = 1;
    long largest_product = 0;

    if (span > digit_count) {
        return -1;
    }
    if (!span && !digit_count) {
        return 1;
    }
    for (long i = 0; i < digit_count; i++) {
        long current = digits[i];

        if (!is_digit(current)) {
            return -1;
        }
        long to_add = to_int(current);

        if (i >= span) {
            long leaving = digits[i - span];
            long to_remove = to_int(leaving);

            if (to_remove == 0) {
                zeros--;
            } else {
                product /= to_remove;
            }
        }
        if (to_add > 0) {
            product *= to_add;
        } else {
            zeros++;
        }
        if ((i + 1 >= span) && (zeros == 0)) {
            if (largest_product > product) {
                largest_product = largest_product;
            } else {
                largest_product = product;
            }
        }
    }
    return largest_product;
}
