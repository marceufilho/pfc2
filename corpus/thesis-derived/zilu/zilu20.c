#include "pfc.h"

long zilu20(long i, long n, long sum)
{
    REQUIRES(i == 0 && n >= 0 && n <= 100 && sum == 0);
    while (i < n) {
        INVARIANT(sum >= 0 && i >= 0);
        sum = sum + i;
        i = i + 1;
    }
    ASSERT(sum >= 0);
    return sum;
}
