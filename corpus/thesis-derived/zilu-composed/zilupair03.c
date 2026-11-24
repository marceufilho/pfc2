#include "pfc.h"

long zilupair03(long n, long sum, long i, long x2, long y2, long steps2)
{
    REQUIRES(n >= 0 && sum == 0 && i == 0 && x2 == 1 && y2 == 1 && 0 <= steps2);
    long step2 = 0;
    while (i < n) {
        INVARIANT(sum >= 0 && i >= 0);
        sum = sum + i;
        i = i + 1;
    }
    ASSERT(sum >= 0);
    while (step2 < steps2) {
        INVARIANT(x2 >= 1 && y2 >= 1);
        x2 = x2 + y2;
        y2 = x2;
        step2 = step2 + 1;
    }
    ASSERT(y2 >= 1);
    return sum;
}
