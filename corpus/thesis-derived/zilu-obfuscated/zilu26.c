/* pfc structured IR round-trip; annotations are unverified. */
#include "pfc.h"

long zilu26(long v0, long v1)
{
    REQUIRES((v0 < v1));
    while ((v0 < v1)) {
        INVARIANT((v0 <= v1));
        v0 = (1 + v0);
    }
    ASSERT((v1 == v0));
    return v0;
}
