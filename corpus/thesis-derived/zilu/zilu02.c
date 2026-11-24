#include "pfc.h"

long zilu02(long n, long l)
{
    REQUIRES(l > 0);
    long i = l;
    while (i < n) {
        INVARIANT(l > 0);
        i = i + 1;
    }
    ASSERT(l >= 1);
    return i;
}
