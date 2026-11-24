/* pfc structured IR round-trip; annotations are unverified. */
#include "pfc.h"

long zilu16(long v1, long v2, long v0)
{
    REQUIRES(((((0 <= v2) && (v2 <= 1)) && (1 == v1)) && (0 <= v0)));
    long v3 = 0;
    while ((v3 < v0)) {
        INVARIANT((((1 <= (v2 + v1)) && ((v2 + v1) <= 2)) && (v1 >= 1)));
        v1 = (1 + v1);
        v2 = (v2 - 1);
        v3 = (1 + v3);
    }
    ASSERT((((1 <= (v2 + v1)) && ((v2 + v1) <= 2)) && (v1 >= 1)));
    return v1;
}
