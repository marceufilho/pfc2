/* pfc structured IR round-trip; annotations are unverified. */
#include "pfc.h"

long zilu29(long v0, long v1)
{
    REQUIRES((v0 < v1));
    while ((v0 < v1)) {
        INVARIANT((v0 <= (99 + v1)));
        v0 = (100 + v0);
    }
    ASSERT(((v0 >= v1) && (v0 <= (99 + v1))));
    return v0;
}
