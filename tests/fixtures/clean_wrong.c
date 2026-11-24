#include "pfc.h"

long count(long n)
    requires(0 <= n)
    ensures(result == n)
{
    long i = 0;

    while (i < n) invariant(1 <= i && i <= n) {
        i = i + 1;
    }
    return i;
}
