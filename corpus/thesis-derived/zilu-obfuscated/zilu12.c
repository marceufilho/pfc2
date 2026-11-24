/* pfc structured IR round-trip; annotations are unverified. */
#include "pfc.h"

long zilu12(long v2, long v1, long v0, long v4)
{
    REQUIRES((((v1 != v2) && (v0 == v1)) && (0 <= v4)));
    long v3 = 0;
    while ((v3 < v4)) {
        INVARIANT((v1 >= v0));
        if ((v2 > 0)) {
            v1 = (v2 + v1);
        }
        v3 = (1 + v3);
    }
    ASSERT((v1 >= v0));
    return v1;
}
