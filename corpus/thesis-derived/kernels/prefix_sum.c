#include "pfc.h"

long prefix_sum(long a[], long a_len, long n)
{
    REQUIRES(0 <= n && n <= a_len);
    if (n == 0) {
        return 0;
    }
    long i = 1;
    while (i < n) {
        INVARIANT(1 <= i && i <= n);
        a[i] = a[i] + a[i - 1];
        i = i + 1;
    }
    return n;
}
