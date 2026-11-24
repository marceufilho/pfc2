#include "pfc.h"

long count(long n)
    requires(0 <= n)
    ensures(result == n)
{
    long i = 0;

    while (i < n) invariant(0 <= i && i <= n) {
        i = i + 1;
    }
    return i;
}

law count_is_never_negative(long n where(0 <= n))
{
    long r = count(n);
    assert(r >= 0);
}
