/* pfc structured IR round-trip; annotations are unverified. */
#include "pfc.h"

long zilu17(long v0, long v2, long v1)
{
    REQUIRES(((0 == v0) && (0 == v2)));
    while ((v0 < v1)) {
        INVARIANT((v2 == v0));
        v0 = (1 + v0);
        v2 = (1 + v2);
    }
    ASSERT((v2 >= v1));
    return v2;
}
