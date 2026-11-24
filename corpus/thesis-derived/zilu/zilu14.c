#include "pfc.h"

long zilu14(long i)
{
    REQUIRES(i >= 0 && i <= 200);
    while (i > 0) {
        INVARIANT(i >= 0);
        i = i - 1;
    }
    ASSERT(i >= 0);
    return i;
}
