#include "pfc.h"

long count(long n)
{
    long i = 0;

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
