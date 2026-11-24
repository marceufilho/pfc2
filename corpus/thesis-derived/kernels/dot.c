#include "pfc.h"

long dot(const long a[], long a_len, const long b[], long b_len, long n)
{
    REQUIRES(0 <= n && n <= a_len && n <= b_len);
    long s = 0;
    long i = 0;
    while (i < n) {
        INVARIANT(0 <= i && i <= n);
        s = s + a[i] * b[i];
        i = i + 1;
    }
    return s;
}
