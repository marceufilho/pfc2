#include "pfc.h"

_Bool is_prime(long n)
    ensures(n < 2 || n > 3 || result)
    ensures(!result || n <= 2 || n % 2 != 0)
{
    for (long i = 2; (i * i) < (n + 1); ++i) invariant(2 <= i && (i == 2 || n % 2 != 0)) {
        if (n % i == 0) {
            return 0;
        }
    }
    return 1;
}

/* The n-th prime, or 0 for n < 1. Upstream writes `if (is_prime(++candidate))`; the update is its own
 * statement (P14). */
long nth_prime(long n)
    ensures(n >= 1 || result == 0)
    ensures(n < 1 || result >= n + 1)
{
    long candidate = 1;
    long count = 0;

    if (n < 1) {
        return 0;
    }
    while (count < n) invariant(0 <= count && count <= n && count < candidate) {
        ++candidate;
        if (is_prime(candidate)) {
            count++;
        }
    }
    return candidate;
}
