#include "pfc.h"

long fill(long a[], long a_len, long n where(0 <= n && n <= a_len))
{
    long i where(0 <= i && i <= n) = 0;

    while (i < n) {
        a[i] = 0;
        i = i + 1;
    }
    return i;
}
