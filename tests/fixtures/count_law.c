#include "pfc.h"

long count(long n)
    requires(0 <= n)
    ensures(result == n)
{
    long i where(0 <= i && i <= n) = 0;

    while (i < n) {
        i = i + 1;
    }
    return i;
}

law count_reaches_n(long n where(0 <= n))
{
    long r = count(n);
    assert(r == n);
}
