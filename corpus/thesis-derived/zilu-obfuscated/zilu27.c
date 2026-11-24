/* pfc structured IR round-trip; annotations are unverified. */
#include "pfc.h"

long zilu27(long v0, long v2, long v1)
{
    REQUIRES(((v0 < v2) && (v1 > (v0 - v2))));
    while ((v0 < v2)) {
        INVARIANT((v1 > (v0 - v2)));
        v1 = (1 + v1);
        v0 = (1 + v0);
    }
    ASSERT((v1 > 0));
    return v1;
}
