#include "pfc.h"

long zilupair14(long i, long k, long n, long x2, long steps2)
{
    REQUIRES(i == 0 && k == 0 && n > 0 && (x2 == 1 || x2 == 2) && 0 <= steps2);
    long step2 = 0;
    while (i < n) {
        INVARIANT(i == k && i <= n);
        i = i + 1;
        k = k + 1;
    }
    ASSERT(i == k && k == n);
    while (step2 < steps2) {
        INVARIANT(x2 == 1 || x2 == 2);
        if (x2 == 1) {
            x2 = 2;
        } else {
            if (x2 == 2) {
                x2 = 1;
            }
        }
        step2 = step2 + 1;
    }
    ASSERT(x2 <= 8);
    return k;
}
