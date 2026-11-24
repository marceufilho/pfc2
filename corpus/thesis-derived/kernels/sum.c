#include "pfc.h"

long sum(const long a[], long a_len, long n)
{
    REQUIRES(0 <= n && n <= a_len);
    long s = 0;
    long i = 0;

    while (i < n) {
        INVARIANT(0 <= i && i <= n);
        s = s + a[i];
        i = i + 1;
    }

    return s;
}
