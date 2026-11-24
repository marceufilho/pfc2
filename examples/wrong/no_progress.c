#include "pfc.h"

/* The body never moves `left`, so the measure does not decrease. Refused at line 9. */
long countdown(long n)
    requires(0 <= n)
{
    long left = n;

    while (left > 0) decreases(left) {
        left = left;
    }
    return left;
}
