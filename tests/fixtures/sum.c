#include "pfc.h"

long sum(const long a[], long a_len, long n where(0 <= n && n <= a_len))
{
    long s = 0;
    long i where(0 <= i && i <= n) = 0;

    while (i < n) {
        s = s + a[i];
        i = i + 1;
    }
    return s;
}
