#include "pfc.h"

/* Verina verina_basic_28: 1 when n (at least 2) is prime, else 0. */
long isPrime(long n)
    requires(n >= 2)
    ensures(result == 0 || result == 1)
{
    for (long k = 2; k < n; k++) invariant(2 <= k && k <= n) decreases(n - k) {
        if (n % k == 0) {
            return 0;
        }
    }
    return 1;
}
