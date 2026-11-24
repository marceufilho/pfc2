#include "pfc.h"

long twice(long n)
    requires(0 <= n && n <= 1000)
    ensures(result == 2 * n)
{
    long i = 0;
    long s = 0;

    while (i < n) {
        s = s + 2;
        i = i + 1;
    }
    return s;
}

law twice_is_double(long n where(0 <= n && n <= 1000))
{
    long r = twice(n);
    assert(r == 2 * n);
}
