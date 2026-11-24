#include "pfc.h"

_Bool is_prime(long n)
{
    for (long i = 2; (i * i) < (n + 1); ++i) {
        if (n % i == 0) {
            return 0;
        }
    }
    return 1;
}

/* The n-th prime, or 0 for n < 1. Upstream writes `if (is_prime(++candidate))`; the update is its own
 * statement (P14). */
long nth_prime(long n)
{
    long candidate = 1;
    long count = 0;

    if (n < 1) {
        return 0;
    }
    while (count < n) {
        ++candidate;
        if (is_prime(candidate)) {
            count++;
        }
    }
    return candidate;
}
