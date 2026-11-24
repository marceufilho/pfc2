/* pfc structured IR round-trip; annotations are unverified. */
#include "pfc.h"

long zilu22(long v1, long v2, long v0)
{
    REQUIRES((((1 == v1) && (0 == v2)) && (0 <= v0)));
    long v3 = 0;
    while ((v3 < v0)) {
        INVARIANT((((v1 >= v2) && (v2 >= 0)) && (v1 >= 1)));
        v1 = (v2 + v1);
        v2 = (1 + v2);
        v3 = (1 + v3);
    }
    ASSERT((v1 >= v2));
    return v1;
}
