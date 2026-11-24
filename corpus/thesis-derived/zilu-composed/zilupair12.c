#include "pfc.h"

long zilupair12(long i, long n, long sum, long x2, long y2, long steps2)
{
    REQUIRES(i == 0 && n >= 0 && n <= 100 && sum == 0 && x2 == 1 && y2 == 0 && 0 <= steps2);
    long step2 = 0;
    while (i < n) {
        INVARIANT(sum >= 0 && i >= 0);
        sum = sum + i;
        i = i + 1;
    }
    ASSERT(sum >= 0);
    while (step2 < steps2) {
        INVARIANT(x2 >= y2 && y2 >= 0 && x2 >= 1);
        x2 = x2 + y2;
        y2 = y2 + 1;
        step2 = step2 + 1;
    }
    ASSERT(x2 >= y2);
    return sum;
}
