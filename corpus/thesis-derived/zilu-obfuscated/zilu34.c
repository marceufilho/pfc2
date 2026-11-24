/* pfc structured IR round-trip; annotations are unverified. */
#include "pfc.h"

long zilu34(long v0, long v2, long v1)
{
    REQUIRES((((0 == v0) && (v1 == v2)) && (v1 > 0)));
    while (((v0 < v1) && (v1 > 0))) {
        INVARIANT(((v1 == (v2 + v0)) && (v0 <= v1)));
        v0 = (1 + v0);
        v2 = (v2 - 1);
    }
    ASSERT((0 == v2));
    return v2;
}
