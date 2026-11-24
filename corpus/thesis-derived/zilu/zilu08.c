#include "pfc.h"

long zilu08(long n, long sum, long i)
{
    REQUIRES(n >= 0 && sum == 0 && i == 0);
    while (i < n) {
        INVARIANT(sum >= 0 && i >= 0);
        sum = sum + i;
        i = i + 1;
    }
    ASSERT(sum >= 0);
    return sum;
}
