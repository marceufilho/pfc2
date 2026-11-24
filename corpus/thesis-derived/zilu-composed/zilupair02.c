#include "pfc.h"

long zilupair02(long i, long k, long n, long i2, long j2)
{
    REQUIRES(i == 0 && k == n && n >= 0 && i2 == 0 && j2 == 0);
    while (i < n) {
        INVARIANT(2 * k + i == 2 * n && i <= n + 1);
        k = k - 1;
        i = i + 2;
    }
    ASSERT(2 * k >= n - 1);
    while (i2 < 100) {
        INVARIANT(j2 == 2 * i2 && i2 <= 100);
        j2 = j2 + 2;
        i2 = i2 + 1;
    }
    ASSERT(j2 == 200);
    return k;
}
